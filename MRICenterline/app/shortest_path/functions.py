import torch
import numpy as np
import SimpleITK as sitk
import statistics
from scipy import ndimage


def create_circle_directions(num_pts=16):
    theta = np.linspace(0, 2*np.pi, num_pts+1)[:-1]
    circle_directions = np.zeros((num_pts, 2))
    circle_directions[:, 0] = np.cos(theta)
    circle_directions[:, 1] = np.sin(theta)
    return circle_directions


def extract_patch(annotation, img, patch_len, patch_pixels_len):
    x_idx = int(annotation[0])
    y_idx = int(annotation[1])
    z_idx = int(annotation[2])
    d = round(patch_len / (2 * img.GetSpacing()[0]))
    image_nda = sitk.GetArrayFromImage(img)

    patch = image_nda[z_idx, (y_idx - d):(y_idx + d + 1), (x_idx - d):(x_idx + d + 1)]
    pad_x_left = np.abs(x_idx - d) if (x_idx - d) <= 0 else 0
    pad_x_right = (x_idx + d + 1 - image_nda.shape[2]) if (x_idx + d + 1) >= image_nda.shape[2] else 0
    pad_y_left = np.abs(y_idx - d) if (y_idx - d) <= 0 else 0
    pad_y_right = (y_idx + d + 1 - image_nda.shape[1]) if (y_idx + d + 1) >= image_nda.shape[1] else 0
    if (y_idx - d) <= 0 or (y_idx + d + 1) >= image_nda.shape[1] or (x_idx - d) <= 0 or (x_idx + d + 1) >= image_nda.shape[2]:
        # print(f'{pad_y_left=}, {pad_y_right=}, {pad_x_left=}, {pad_x_right=}, {x_idx=}, {y_idx=}, {d=}, {image_nda.shape=}, {patch.shape}')
        patch = np.pad(patch, [(pad_y_left, pad_y_right), (pad_x_left, pad_x_right)], mode='constant')
    zoom_factor = patch_pixels_len / (2 * d + 1)
    patch = ndimage.zoom(patch, [zoom_factor, zoom_factor])
    patch = torch.from_numpy(patch.astype(np.int16)).float()
    return patch


def convert_16dir_to_8dir(label_pred_proba_16):
    label_pred_proba_8 = []
    normalized_label_pred_proba_8 = []
    label_pred_proba_16 = label_pred_proba_16.numpy()
    # weights = [0.25, 0.5, 0.25]
    for i, prob in enumerate(label_pred_proba_16):
        if i % 2 == 0:
            prev_prob = label_pred_proba_16[(i - 1) % 16]
            next_prob = label_pred_proba_16[(i + 1) % 16]
            new_prob = statistics.mean([prev_prob, prob, next_prob])
            new_prob = np.exp(-new_prob)
            label_pred_proba_8.append(new_prob)
    prob_8_sum = sum(label_pred_proba_8)
    for i, prob_8 in enumerate(label_pred_proba_8):
        normalized_label_pred_proba_8.append(prob_8 / prob_8_sum)
    return normalized_label_pred_proba_8


def check_limits(x, y, i, j, x_len, y_len):
    if i == 0 and j == 0 or x + i < 0 or y + j < 0 or (x + i) >= x_len or (y + j) >= y_len:
        return False
    return True


def match_prob(i, j, label_pred_proba_8):
    # print(f'{i=}, {j=}')
    if i == 1 and j == 0:
        return label_pred_proba_8[0]
    if i == 1 and j == 1:
        return label_pred_proba_8[1]
    if i == 0 and j == 1:
        return label_pred_proba_8[2]
    if i == -1 and j == 1:
        return label_pred_proba_8[3]
    if i == -1 and j == 0:
        return label_pred_proba_8[4]
    if i == -1 and j == -1:
        return label_pred_proba_8[5]
    if i == 0 and j == -1:
        return label_pred_proba_8[6]
    if i == 1 and j == -1:
        return label_pred_proba_8[7]
    # print(f'wrong coordinates! {i=}, {j=}')
    return None


def calc_graph_weights(init_x, init_y, num_of_pixels, x_len, y_len, slice, img, patch_len, grid_pixel_size, model, device):
    # from pathlib import Path
    # return np.load(str(Path(__file__).parent / "6.npy"))

    # TODO: make this more efficient
    graph = np.zeros((num_of_pixels, num_of_pixels))

    for x in range(x_len):
        for y in range(y_len):
            pixel = np.array([init_x + x, init_y + y, slice])
            patch = extract_patch(pixel, img, patch_len, grid_pixel_size[0])
            patch = torch.unsqueeze(patch, 0)
            with torch.no_grad():
                label_pred = model(patch.to(device))
            label_pred_proba_16 = model.predict_proba_scores(label_pred.to(device)).cpu()
            label_pred_proba_8 = convert_16dir_to_8dir(label_pred_proba_16[0])
            pixel_single_cord = y * x_len + x
            # if pixel_single_cord == 303: print(f'{pixel_single_cord=}, {x=}, {y=}')
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if check_limits(x, y, i, j, x_len, y_len):
                        neighbor_single_cord = (y+j) * x_len + (x+i)
                        prob = match_prob(i, j, label_pred_proba_8)
                        if prob is not None:
                            graph[pixel_single_cord][neighbor_single_cord] = np.exp(-prob)

            print(f"Graph weights: {round(x / x_len, 2)}, {round(y / y_len, 2)}")

    return graph


def extract_roi(case_sitk, slice_num, first_annotation, second_annotation):
    from MRICenterline.app.shortest_path.find import GRID_PIXELS_SIZE

    image_nda = sitk.GetArrayFromImage(case_sitk)
    len = case_sitk.GetSize()

    min_x = np.min((first_annotation[0], second_annotation[0]))
    max_x = np.max((first_annotation[0], second_annotation[0]))
    min_y = np.min((first_annotation[1], second_annotation[1]))
    max_y = np.max((first_annotation[1], second_annotation[1]))

    init_x = round(min_x - 0.5 * GRID_PIXELS_SIZE[0] if min_x >= (0.5 * GRID_PIXELS_SIZE[0]) else 0)
    final_x = round(max_x + 0.5 * GRID_PIXELS_SIZE[0] if max_x < (len[0] - 0.5 * GRID_PIXELS_SIZE[0]) else (len[0]-1))
    init_y = round(min_y - 0.5 * GRID_PIXELS_SIZE[1] if min_y >= (0.5 * GRID_PIXELS_SIZE[1]) else 0)
    final_y = round(max_y + 0.5 * GRID_PIXELS_SIZE[1] if max_y < (len[1] - 0.5 * GRID_PIXELS_SIZE[1]) else (len[1] - 1))

    roi = image_nda[slice_num, init_y:final_y + 1, init_x:final_x + 1]

    return roi, init_x, final_x, init_y, final_y


def convert_1Dcord_to_2Dcord(_1Dcord, x_len, init_x, init_y):
    _2Dcord = np.zeros((2, len(_1Dcord)))
    for i, cord in enumerate(_1Dcord):
        _2Dcord[1, i] = init_y + np.floor(cord / x_len)
        _2Dcord[0, i] = init_x + cord % x_len

        # _2Dcord[1, i] = np.floor(cord / x_len)
        # _2Dcord[0, i] = cord % x_len
    return _2Dcord
