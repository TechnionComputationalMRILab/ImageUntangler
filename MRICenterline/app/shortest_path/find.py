import numpy as np
from pathlib import Path
from MRICenterline.app.shortest_path.compile import unpack_saved_graph
from MRICenterline import CFG

GRID_SPACING = (1.5, 1.5, 1.5)
GRID_PIXELS_SIZE = (32, 32)
CIRCLE_DIRECTIONS_NUM = 16
PATCH_LEN = GRID_SPACING[0] * GRID_PIXELS_SIZE[0]


def find_shortest_path(case_sitk, annotation_points, case_number):
    unique_slices, slice_counts = np.unique(annotation_points[:, 2], return_counts=True)

    total_track = []

    for slice_num, slice_count in zip(unique_slices, slice_counts):
        if slice_count == 1:  # it's the only dot in its slice
            slice_point = np.squeeze(annotation_points[np.where(annotation_points[:, 2] == slice_num), :])
            total_track.append(list(slice_point))
        else:
            slice_points = np.squeeze(annotation_points[np.where(annotation_points[:, 2] == slice_num), :])
            assert len(slice_points) == 2
            # otherwise it means that there's more than two points in the slice

            shortest_path_in_slice, _ = FindShortestPathPerSlice(case_sitk=case_sitk,
                                                                 slice_num=slice_num,
                                                                 first_annotation=slice_points[1],
                                                                 second_annotation=slice_points[0],
                                                                 case_number=case_number)

            for pt in list(zip(
                    shortest_path_in_slice[0][0],
                    shortest_path_in_slice[0][1],
                    [slice_num]*len(shortest_path_in_slice[0][1])
            )):
                total_track.append(pt)

    return np.array(total_track, dtype=int)


# input(1): slice as numpy array
# input(2): numpy array of size 2 for the coordinates of the first annotation
# input(3): numpy array of size 2 for the coordinates of the second annotation
def FindShortestPathPerSlice(case_sitk, slice_num, first_annotation, second_annotation, case_number):
    if CFG.torch_cuda_available:
        import torch
        x_spline_gt = torch.load(Path(CFG.get_folder("model", "shortest_path")) / 'x_spline_gt.pt')
        y_spline_gt = torch.load(Path(CFG.get_folder("model", "shortest_path")) / 'y_spline_gt.pt')
    else:
        import numpy as np
        x_spline_gt = np.load(str(Path(CFG.get_folder("model", "shortest_path")) / 'x_spline_gt.npy'))
        y_spline_gt = np.load(str(Path(CFG.get_folder("model", "shortest_path")) / 'y_spline_gt.npy'))

    from MRICenterline.app.shortest_path.Graph import Graph
    from MRICenterline.app.shortest_path.functions import extract_roi, convert_1Dcord_to_2Dcord, calc_contrast_mean_std

    a = [0.49026966, 0.51766915, 0.4897049]

    # slice 22
    roi_nda, \
        roi_init_x, roi_final_x, \
        roi_init_y, roi_final_y = extract_roi(case_sitk, slice_num,
                                              first_annotation, second_annotation)

    roi_x_len = roi_final_x - roi_init_x + 1
    roi_y_len = roi_final_y - roi_init_y + 1
    roi_num_of_pixels = roi_x_len * roi_y_len

    g = Graph(roi_num_of_pixels)

    import numpy as np
    saved_graph = np.load(str(Path(CFG.get_folder("model", "shortest_path", "saved_graph", case_number)) / f"{slice_num}.npy"))
    unpack_saved_graph(saved_graph, g.graph, case_sitk.GetSize()[0:2],
                       roi_x=(roi_init_x, roi_final_x, roi_x_len),
                       roi_y=(roi_init_y, roi_final_y, roi_y_len))

    # mean, var, _ = calc_contrast_mean_std(x_spline_gt, y_spline_gt, roi_init_x, roi_init_y, roi_nda)
    # TODO: ???
    mean = 1580.0457142857142
    var = 29000.317910204078

    sp_2Dcord = []

    print("Calculating shortest path coordinates")
    # for j in range(2):
    j = 1
    first_pixel = first_annotation if j == 0 else second_annotation
    final_pixel = second_annotation if j == 0 else first_annotation

    first_pixel_1DCord = int((first_pixel[1] - roi_init_y) * roi_x_len + (first_pixel[0] - roi_init_x))
    final_pixel_1DCord = int((final_pixel[1] - roi_init_y) * roi_x_len + (final_pixel[0] - roi_init_x))

    g.dijkstra(src=first_pixel_1DCord, dest=final_pixel_1DCord,
               len_x=roi_x_len, len_y=roi_y_len,
               a=a, slice_nda=roi_nda,
               init_x=roi_init_x, init_y=roi_init_y,
               mean=mean, var=var
               )

    sp_1Dcord = g.track_sp(first_pixel_1DCord, final_pixel_1DCord)
    sp_2Dcord.append(convert_1Dcord_to_2Dcord(sp_1Dcord, roi_x_len, roi_init_x, roi_init_y))

    return sp_2Dcord, roi_nda
