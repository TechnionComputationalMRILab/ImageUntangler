import torch
from pathlib import Path
from MRICenterline.app.shortest_path.compile import unpack_saved_graph

GRID_SPACING = (1.5, 1.5, 1.5)
GRID_PIXELS_SIZE = (32, 32)
CIRCLE_DIRECTIONS_NUM = 16
PATCH_LEN = GRID_SPACING[0] * GRID_PIXELS_SIZE[0]


# input(1): slice as numpy array
# input(2): numpy array of size 2 for the coordinates of the first annotation
# input(3): numpy array of size 2 for the coordinates of the second annotation
def FindShortestPathPerSlice(case_sitk, slice_num, first_annotation, second_annotation, case_number):
    from MRICenterline.app.shortest_path.Graph import Graph
    from MRICenterline.app.shortest_path.functions import extract_roi, convert_1Dcord_to_2Dcord

    a = [0.49026966, 0.51766915, 0.4897049]

    x_spline_gt = torch.load(Path(__file__).parent / 'x_spline_gt.pt')
    y_spline_gt = torch.load(Path(__file__).parent / 'y_spline_gt.pt')

    roi_nda, \
        roi_init_x, roi_final_x, \
        roi_init_y, roi_final_y = extract_roi(case_sitk, slice_num,
                                              first_annotation, second_annotation)

    roi_x_len = roi_final_x - roi_init_x + 1
    roi_y_len = roi_final_y - roi_init_y + 1
    roi_num_of_pixels = roi_x_len * roi_y_len

    g = Graph(roi_num_of_pixels)

    import numpy as np
    saved_graph = np.load(str(Path(__file__).parent / "saved_graph" / "6.npy"))  # TODO: generalize this
    unpack_saved_graph(saved_graph, g.graph, case_sitk.GetSize()[0:2],
                       roi_x=(roi_init_x, roi_final_x, roi_x_len),
                       roi_y=(roi_init_y, roi_final_y, roi_y_len))

    sp_2Dcord = []

    print("Calculating shortest path coordinates")
    # for j in range(2):
    j = 1
    first_pixel = first_annotation if j == 0 else second_annotation
    final_pixel = second_annotation if j == 0 else first_annotation

    first_pixel_1DCord = (first_pixel[1] - roi_init_y) * roi_x_len + (first_pixel[0] - roi_init_x)
    final_pixel_1DCord = (final_pixel[1] - roi_init_y) * roi_x_len + (final_pixel[0] - roi_init_x)

    g.dijkstra(int(first_pixel_1DCord), final_pixel_1DCord, roi_x_len, roi_y_len, a, roi_nda, roi_init_x, roi_init_y, x_spline_gt, y_spline_gt)

    sp_1Dcord = g.track_sp(first_pixel_1DCord, final_pixel_1DCord)
    sp_2Dcord.append(convert_1Dcord_to_2Dcord(sp_1Dcord, roi_x_len, roi_init_x, roi_init_y))

    return sp_2Dcord, roi_nda
