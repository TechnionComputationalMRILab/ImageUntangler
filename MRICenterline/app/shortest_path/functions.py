import numpy as np
import SimpleITK as sitk
import statistics


def create_circle_directions(num_pts=16):
    theta = np.linspace(0, 2 * np.pi, num_pts + 1)[:-1]
    circle_directions = np.zeros((num_pts, 2))
    circle_directions[:, 0] = np.cos(theta)
    circle_directions[:, 1] = np.sin(theta)
    return circle_directions


def convert_16dir_to_8dir(label_pred_proba_16):
    label_pred_proba_8 = []
    normalized_label_pred_proba_8 = []
    label_pred_proba_16 = label_pred_proba_16.numpy()
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


def extract_roi(case_sitk, slice_num, first_annotation, second_annotation):
    from MRICenterline.app.shortest_path.find import GRID_PIXELS_SIZE

    image_nda = sitk.GetArrayFromImage(case_sitk)
    len = case_sitk.GetSize()

    min_x = np.min((first_annotation[0], second_annotation[0]))
    max_x = np.max((first_annotation[0], second_annotation[0]))
    min_y = np.min((first_annotation[1], second_annotation[1]))
    max_y = np.max((first_annotation[1], second_annotation[1]))

    init_x = round(min_x - 0.5 * GRID_PIXELS_SIZE[0] if min_x >= (0.5 * GRID_PIXELS_SIZE[0]) else 0)
    final_x = round(max_x + 0.5 * GRID_PIXELS_SIZE[0] if max_x < (len[0] - 0.5 * GRID_PIXELS_SIZE[0]) else (len[0] - 1))
    init_y = round(min_y - 0.5 * GRID_PIXELS_SIZE[1] if min_y >= (0.5 * GRID_PIXELS_SIZE[1]) else 0)
    final_y = round(max_y + 0.5 * GRID_PIXELS_SIZE[1] if max_y < (len[1] - 0.5 * GRID_PIXELS_SIZE[1]) else (len[1] - 1))

    roi = image_nda[slice_num, init_y:final_y + 1, init_x:final_x + 1]
    # roi = image_nda[slice_num, :, :]

    return roi, init_x, final_x, init_y, final_y


def convert_1Dcord_to_2Dcord(_1Dcord, x_len, init_x, init_y):
    _2Dcord = np.zeros((2, len(_1Dcord)))
    for i, cord in enumerate(_1Dcord):
        _2Dcord[1, i] = init_y + np.floor(cord / x_len)
        _2Dcord[0, i] = init_x + cord % x_len

        # _2Dcord[1, i] = np.floor(cord / x_len)
        # _2Dcord[0, i] = cord % x_len
    return _2Dcord


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
