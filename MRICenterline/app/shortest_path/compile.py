# import numba
import numpy as np


# @numba.njit(cache=True, nogil=True)
def unpack_saved_graph(saved_graph, graph, sitk_image_size, roi_x, roi_y):
    # saved_graph = np.load(saved_graph_path)
    init_x, init_y = 0, 0
    x_len, y_len = sitk_image_size

    roi_init_x, roi_final_x, roi_x_len = roi_x
    roi_init_y, roi_final_y, roi_y_len = roi_y

    def convert_1Dcord_to_2Dcord(_1Dcord, x_len, init_x, init_y):
        _2Dcord = np.zeros((2, len(_1Dcord)))
        for i, cord in enumerate(_1Dcord):
            _2Dcord[1, i] = init_y + np.floor(cord / x_len)
            _2Dcord[0, i] = init_x + cord % x_len
        return _2Dcord

    for temp_x in range(roi_init_x, roi_final_x):
        for temp_y in range(roi_init_y, roi_final_y):
            for j in range(8):
                slice_temp_single_cord = temp_y * x_len + temp_x
                neighbor_single_cord = saved_graph[slice_temp_single_cord][j][1]

                x, y = convert_1Dcord_to_2Dcord([int(neighbor_single_cord)], x_len, init_x, init_y)
                x = int(x[0])
                y = int(y[0])

                if not (x < roi_init_x or y < roi_init_y or x > roi_final_x or y > roi_final_y):
                    roi_neighbor_single_cord = (y - roi_init_y) * roi_x_len + (x - roi_init_x)

                    i = (temp_y - roi_init_y) * roi_x_len + (temp_x - roi_init_x)

                    prob = saved_graph[slice_temp_single_cord][j][0]
                    graph[i][int(roi_neighbor_single_cord)] = prob


# @numba.njit(nogil=True)
def compiled_dijkstra(V, graph_parent, graph, src, len_x, len_y, a, slice_nda, init_x, init_y, x_spline_gt, y_spline_gt):
    def create_circle_directions(num_pts=16):
        theta = np.linspace(0, 2 * np.pi, num_pts + 1)[:-1]
        circle_directions = np.zeros((num_pts, 2))
        circle_directions[:, 0] = np.cos(theta)
        circle_directions[:, 1] = np.sin(theta)
        return circle_directions

    def calc_contrast_mean_std(x_spline_gt, y_spline_gt, init_x, init_y, slice_nda):
        x_spline_gt_shifted = x_spline_gt - init_x
        y_spline_gt_shifted = y_spline_gt - init_y
        spline_val = []
        for i in range(len(x_spline_gt)):
            spline_val.append(slice_nda[int(y_spline_gt_shifted[i]), int(x_spline_gt_shifted[i])])
        mean = np.mean(spline_val)
        var = np.var(spline_val)
        std = np.sqrt(var)
        return mean, var, std

    def minDistance(dist, sptSet):
        non_zero_arr = np.nonzero(dist * ~sptSet)
        min_index = non_zero_arr[0][np.argmin(dist[non_zero_arr])]
        return min_index

    def is_out_of_patch(x, n, len_x, len_y):
        if x % len_x == 0 and n in [-(len_x + 1), -1, (len_x - 1)] or \
            x % len_x == (len_x - 1) and n in [-(len_x - 1), 1, (len_x + 1)] or \
            x / len_x == 0 and n in [-(len_x - 1), -len_x, -(len_x + 1)] or \
            x / len_x == (len_y - 1) and n in [(len_x - 1), len_x, (len_x + 1)]:
            return True
        return False

    def match_dir(diff, len_x, directions):
        if diff == 1:
            return directions[0]
        if diff == (len_x + 1):
            return directions[1]
        if diff == len_x:
            return directions[2]
        if diff == (len_x - 1):
            return directions[3]
        if diff == -1:
            return directions[4]
        if diff == -(len_x + 1):
            return directions[5]
        if diff == -len_x:
            return directions[6]
        if diff == -(len_x - 1):
            return directions[7]

    def calc_angle(d1, d2):
        # print("CALC ANGLE", d1, d2)
        return (np.pi - np.arccos(np.sum(d1 * d2) / (np.sqrt(np.sum(d1 * d1)) * np.sqrt(np.sum(d2 * d2)))))/np.pi

    def convert_1Dcord_to_2Dcord(_1Dcord, x_len, init_x, init_y):
        _2Dcord = np.zeros((2, len(_1Dcord)))
        for i, cord in enumerate(_1Dcord):
            _2Dcord[1, i] = init_y + np.floor(cord / x_len)
            _2Dcord[0, i] = init_x + cord % x_len

            # _2Dcord[1, i] = np.floor(cord / x_len)
            # _2Dcord[0, i] = cord % x_len
        return _2Dcord

    def calc_contrast_var(y, slice_nda, len_x, init_x, init_y, var, mean):

        y2D = convert_1Dcord_to_2Dcord([y], len_x, init_x, init_y)
        contrast_diff = np.abs(slice_nda[int(y2D[1][0]) - init_y, int(y2D[0][0]) - init_x] - mean)
        exp_contrast = 1 - np.exp(-(np.power(contrast_diff, 2))/var)
        return exp_contrast

    dist = np.array([np.inf] * V)
    dist[src] = 0.1
    sptSet = np.array([False] * V)

    graph_parent[src] = -1

    direction = np.array([None] * V)
    directions_8 = create_circle_directions(8)

    mean, var, std = calc_contrast_mean_std(x_spline_gt, y_spline_gt, init_x, init_y, slice_nda)

    neighbors = [-(len_x - 1), -len_x, -(len_x + 1), -1, (len_x - 1), len_x, (len_x + 1), 1]

    for cout in range(V):
        x = minDistance(dist, sptSet)
        sptSet[x] = True

        for n in neighbors:
            if is_out_of_patch(x, n, len_x, len_y): continue
            y = x + n
            if y < 0 or y >= V: continue
            d = match_dir(n, len_x, directions_8)
            if direction[x] is not None:
                # if self.graph[x][y] == 0: print(f'if: graph = 0, {x=}, {y=}, {n=}')
                if graph[x][y] != 0:
                    angle = calc_angle(direction[x], d)
                    exp_cos_angle = np.exp(-angle)
                    exp_contrast = calc_contrast_var(y, slice_nda, len_x, init_x, init_y, var, mean)

                    if sptSet[y] == False and dist[y] > dist[x] + a[0] * graph[x][y] + a[1] * exp_cos_angle + a[2] * exp_contrast:
                        dist[y] = dist[x] + a[0] * graph[x][y] + a[1] * exp_cos_angle + a[2] * exp_contrast
                        graph_parent[y] = x
                        direction[y] = d
            else:
                # if graph[x][y] == 0: print('else: graph = 0')
                # if self.graph[x][y] == 0: assert False, 'else: graph = 0'
                if graph[x][y] != 0 and sptSet[y] == False and \
                        dist[y] > dist[x] + graph[x][y]:
                    dist[y] = dist[x] + graph[x][y]
                    graph_parent[y] = x
                    direction[y] = d

