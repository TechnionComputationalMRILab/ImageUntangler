# # import torch
# from pathlib import Path
# import SimpleITK as sitk
#
#
# GRID_SPACING = (1.5, 1.5, 1.5)
# GRID_PIXELS_SIZE = (32, 32)
# CIRCLE_DIRECTIONS_NUM = 16
# PATCH_LEN = GRID_SPACING[0] * GRID_PIXELS_SIZE[0]
#
#
# # input(1): slice as numpy array
# # input(2): numpy array of size 2 for the coordinates of the first annotation
# # input(3): numpy array of size 2 for the coordinates of the second annotation
# def FindShortestPathPerSlice(case_sitk, slice_num, first_annotation, second_annotation, case_number):
#     from MRICenterline.app.shortest_path import classifier
#     from MRICenterline.app.shortest_path import Net
#     from MRICenterline.app.shortest_path.Graph import Graph
#     from MRICenterline.app.shortest_path.functions import extract_roi, calc_graph_weights, convert_1Dcord_to_2Dcord
#
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#
#     # load model
#     model = classifier.ArgMaxClassifier(
#         model=Net.CNN(in_size=GRID_PIXELS_SIZE, directions_num=2, hidden_dims=[64, CIRCLE_DIRECTIONS_NUM]))
#
#     model_dict_path = Path(__file__).parent / "model_dict" / f"{case_number}.pt"
#     print(f"Loading {model_dict_path}")
#
#     # if torch.cuda.is_available():
#     model.load_state_dict(torch.load(model_dict_path))
#     # else:
#     #     model.load_state_dict(torch.load(model_dict_path, map_location=torch.device('cpu')))
#
#         # os.path.join('/tcmldrive/rotem/sync_thesis', 'db_loop_output_check_seed0', '6', 'model_dict', f'off_samples_from_normal_aug_is_TRUE',
#         #              'model_dict.pt')))
#     model.eval()
#
#     a = [0.49026966, 0.51766915, 0.4897049]
#
#     # gt_path = '/tcmldrive/rotem/thesis/db_include_off_samples_from_normal_check_seed0/ground_truth_spline/FIESTA/case6/slice22/idx2'
#     x_spline_gt = torch.load(Path(__file__).parent / 'x_spline_gt.pt')
#     y_spline_gt = torch.load(Path(__file__).parent / 'y_spline_gt.pt')
#
#     print("Extracting ROI")
#     # roi_nda, init_x, final_x, init_y, final_y = extract_roi(case_sitk, slice_num, first_annotation, second_annotation)
#
#     # CALCULATE EVERYTHING
#     image_nda = sitk.GetArrayFromImage(case_sitk)
#     roi_nda = image_nda[slice_num, :, :]
#
#     init_x, init_y = 0, 0
#     final_x, final_y = case_sitk.GetSize()[0:2]
#
#     x_len = final_x #final_x - init_x + 1
#     y_len = final_y #final_y - init_y + 1
#     num_of_pixels = x_len * y_len
#
#     g = Graph(num_of_pixels)
#     print("Calculating graph weights")
#     g.graph = calc_graph_weights(init_x, init_y, num_of_pixels, x_len, y_len, slice_num, case_sitk, PATCH_LEN,
#                                  GRID_PIXELS_SIZE, model, device)
#     sp_2Dcord = []
#
#     print("Calculating shortest path coordinates")
#     for j in range(2):
#         first_pixel = first_annotation if j == 0 else second_annotation
#         final_pixel = second_annotation if j == 0 else first_annotation
#
#         first_pixel_1DCord = (first_pixel[1] - init_y) * x_len + (first_pixel[0] - init_x)
#         final_pixel_1DCord = (final_pixel[1] - init_y) * x_len + (final_pixel[0] - init_x)
#
#         g.dijkstra(first_pixel_1DCord, x_len, y_len, a, roi_nda, init_x, init_y, x_spline_gt, y_spline_gt)
#
#         sp_1Dcord = g.track_sp(first_pixel_1DCord, final_pixel_1DCord)
#         sp_2Dcord.append(convert_1Dcord_to_2Dcord(sp_1Dcord, x_len, init_x, init_y))
#
#     return sp_2Dcord, roi_nda
