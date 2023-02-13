import numpy as np
import SimpleITK as sitk
from scipy import ndimage

from MRICenterline.app.shortest_path.functions import convert_16dir_to_8dir, check_limits, match_prob


def extract_patch(annotation, img, patch_len, patch_pixels_len):
    import torch

    x_idx = int(annotation[0])
    y_idx = int(annotation[1])
    z_idx = int(annotation[2])
    d = round(patch_len / (2 * img.GetSpacing()[0]))
    image_nda = sitk.GetArrayFromImage(img)

    # patch = image_nda[z_idx, (y_idx - d):(y_idx + d + 1), (x_idx - d):(x_idx + d + 1)]
    pad_x_left = np.abs(x_idx - d) if (x_idx - d) <= 0 else 0
    pad_x_right = (x_idx + d + 1 - image_nda.shape[2]) if (x_idx + d + 1) >= image_nda.shape[2] else 0
    pad_y_left = np.abs(y_idx - d) if (y_idx - d) <= 0 else 0
    pad_y_right = (y_idx + d + 1 - image_nda.shape[1]) if (y_idx + d + 1) >= image_nda.shape[1] else 0
    if (y_idx - d) <= 0 or (y_idx + d + 1) >= image_nda.shape[1] or (x_idx - d) <= 0 or (x_idx + d + 1) >= \
            image_nda.shape[2]:
        x_left = 0 if (x_idx - d) <= 0 else (x_idx - d)
        x_right = image_nda.shape[2] if (x_idx + d + 1) >= image_nda.shape[2] else (x_idx + d + 1)
        y_left = 0 if (y_idx - d) <= 0 else (y_idx - d)
        y_right = image_nda.shape[1] if (y_idx + d + 1) >= image_nda.shape[1] else (y_idx + d + 1)
        patch = image_nda[z_idx, y_left:y_right, x_left:x_right]
        patch = np.pad(patch, [(pad_y_left, pad_y_right), (pad_x_left, pad_x_right)], mode='constant')
    else:
        patch = image_nda[z_idx, (y_idx - d):(y_idx + d + 1), (x_idx - d):(x_idx + d + 1)]
    zoom_factor = patch_pixels_len / (2 * d + 1)
    patch = ndimage.zoom(patch, [zoom_factor, zoom_factor])
    patch = torch.from_numpy(patch.astype(np.int16)).float()
    return patch


def calc_graph_weights(init_x, init_y, num_of_pixels, x_len, y_len,
                       slice_num, img, patch_len, grid_pixel_size, case_number):
    import torch

    from MRICenterline.app.shortest_path import classifier
    from MRICenterline.app.shortest_path import Net
    from MRICenterline.app.shortest_path.find import CIRCLE_DIRECTIONS_NUM, GRID_PIXELS_SIZE
    from pathlib import Path

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model
    model = classifier.ArgMaxClassifier(
        model=Net.CNN(in_size=GRID_PIXELS_SIZE, directions_num=2, hidden_dims=[64, CIRCLE_DIRECTIONS_NUM]))

    model_dict_path = Path(__file__).parent / "model_dict" / f"{case_number}.pt"
    print(f"Loading {model_dict_path}")

    model.load_state_dict(torch.load(model_dict_path))
    model.eval()

    graph = np.zeros((num_of_pixels, 8, 2))  # 2 is the coordinates, 8 is the actual graph value
    model = model.to(device)

    from tqdm import tqdm
    for x in tqdm(range(x_len)):
        for y in range(y_len):

            pixel = np.array([init_x + x, init_y + y, slice_num])
            patch = extract_patch(pixel, img, patch_len, grid_pixel_size[0])

            patch = torch.unsqueeze(patch, 0)
            with torch.no_grad():
                label_pred = model(patch.to(device))

            label_pred_proba_16 = model.predict_proba_scores(label_pred.to(device)).cpu()

            label_pred_proba_8 = convert_16dir_to_8dir(label_pred_proba_16[0])
            pixel_single_cord = y * x_len + x

            index = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if check_limits(x, y, i, j, x_len, y_len):
                        neighbor_single_cord = (y + j) * x_len + (x + i)
                        prob = match_prob(i, j, label_pred_proba_8)
                        if prob is not None:
                            graph[pixel_single_cord][index][0] = np.exp(-prob)
                            graph[pixel_single_cord][index][1] = neighbor_single_cord
                            index += 1
    return graph
