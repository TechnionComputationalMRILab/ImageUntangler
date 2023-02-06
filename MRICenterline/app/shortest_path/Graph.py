import numpy as np

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.parent = [None] * self.V
        self.direction = [None] * self.V
        # self.graph = [[0 for column in range(vertices)]
        #               for row in range(vertices)]
        self.graph = np.zeros((vertices, vertices))

    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node], "\t", "parent: ", self.parent[node])

    def minDistance(self, dist, sptSet):
        non_zero_arr = np.nonzero(dist * ~sptSet)
        min_index = non_zero_arr[0][np.argmin(dist[non_zero_arr])]
        return min_index

    def dijkstra(self, src: int, dest, len_x, len_y, a, slice_nda, init_x, init_y, mean, var):
        from MRICenterline.app.shortest_path.functions import create_circle_directions

        dist = np.array([np.inf] * self.V)
        dist[src] = 0.1
        sptSet = np.array([False] * self.V)

        self.parent[src] = -1

        direction = np.array([None] * self.V)
        directions_8 = create_circle_directions(8)

        neighbors = [-(len_x - 1), -len_x, -(len_x + 1), -1, (len_x - 1), len_x, (len_x + 1), 1]

        for cout in range(self.V):
            x = self.minDistance(dist, sptSet)
            sptSet[x] = True

            if x == dest:
                break

            for n in neighbors:
                if self.is_out_of_patch(x, n, len_x, len_y): continue
                y = x + n
                if y < 0 or y >= self.V: continue
                d = self.match_dir(n, len_x, directions_8)
                if direction[x] is not None:
                    # if self.graph[x][y] == 0: print(f'if: graph = 0, {x=}, {y=}, {n=}')
                    if self.graph[x][y] != 0:
                        angle = self.calc_angle(direction[x], d)
                        exp_cos_angle = np.exp(-angle)
                        exp_contrast = self.calc_contrast_var(y, slice_nda, len_x, init_x, init_y, var, mean)

                        if sptSet[y] == False and dist[y] > dist[x] + a[0] * self.graph[x][y] + a[1] * exp_cos_angle + a[2] * exp_contrast:
                            dist[y] = dist[x] + a[0] * self.graph[x][y] + a[1] * exp_cos_angle + a[2] * exp_contrast
                            self.parent[y] = x
                            direction[y] = d
                else:
                    if self.graph[x][y] == 0: print('else: graph = 0')
                    # if self.graph[x][y] == 0: assert False, 'else: graph = 0'
                    if self.graph[x][y] != 0 and sptSet[y] == False and \
                            dist[y] > dist[x] + self.graph[x][y]:
                        dist[y] = dist[x] + self.graph[x][y]
                        self.parent[y] = x
                        direction[y] = d


    def is_out_of_patch(self, x, n, len_x, len_y):
        if x % len_x == 0 and n in [-(len_x + 1), -1, (len_x - 1)] or \
            x % len_x == (len_x - 1) and n in [-(len_x - 1), 1, (len_x + 1)] or \
            x / len_x == 0 and n in [-(len_x - 1), -len_x, -(len_x + 1)] or \
            x / len_x == (len_y - 1) and n in [(len_x - 1), len_x, (len_x + 1)]:
            return True
        return False

    def track_sp(self, first_annotation, final_annotation):
        pixel = final_annotation
        sp = []
        while pixel != first_annotation:
            sp.append(pixel)
            pixel = self.parent[pixel]
        sp.append(first_annotation)
        return sp

    def match_dir(self, diff, len_x, directions):
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

    def calc_angle(self, d1, d2):
        # print("CALC ANGLE", d1, d2)
        return (np.pi - np.arccos(np.sum(d1 * d2) / (np.sqrt(np.sum(d1 * d1)) * np.sqrt(np.sum(d2 * d2)))))/np.pi

    def calc_contrast_var(self, y, slice_nda, len_x, init_x, init_y, var, mean):
        from MRICenterline.app.shortest_path.functions import convert_1Dcord_to_2Dcord

        y2D = convert_1Dcord_to_2Dcord([y], len_x, init_x, init_y)
        contrast_diff = np.abs(slice_nda[int(y2D[1][0]) - init_y, int(y2D[0][0]) - init_x] - mean)
        exp_contrast = 1 - np.exp(-(np.power(contrast_diff, 2))/var)
        return exp_contrast
