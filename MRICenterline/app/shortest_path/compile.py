import numba
import numpy as np


@numba.njit(cache=True, nogil=True)
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
def compiled_dijkstra():
    pass
