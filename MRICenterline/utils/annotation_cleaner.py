from PyQt5.QtWidgets import QFileDialog
from MRICenterline.Loader.LoadPoints import LoadPoints
from MRICenterline.Points.SaveFormatter import SaveFormatter
import numpy as np
import json
import os
from shutil import copy


def convert(imagedata, bad_z_coords, model):
    print("CONVERTING")

    fixed_z_coords = imagedata.z_coords

    _file, _ = QFileDialog.getOpenFileName(model)
    print(os.path.split(_file))

    copy(_file, os.path.join(os.path.split(_file)[0], "BACKUP__" + os.path.split(_file)[1]))
    lp = LoadPoints(_file, imagedata, get_raw_dataset=True)

    # for i in lp.point_set.values():
    #     for pt in i:
    #         for k, bad_z in enumerate(bad_z_coords):
    #             if np.isclose(pt[2], bad_z):
    #                 pass
                    # print(f"replace {bad_z} with {fixed_z_coords[k]}")

    with open(_file, 'r') as f:
        json_data = json.load(f)

    _save_formatter = SaveFormatter(imagedata, append_to_directory=False, path=os.path.split(_file)[0])

    _fix = []
    for i in lp.point_set.keys():
        print(i)
        _list = []
        for pt in json_data[i]:
            for k, bad_z in enumerate(bad_z_coords):
                if np.isclose(pt[2], bad_z):
                    print(f"replace {bad_z} with {fixed_z_coords[k]}")
                    _list.append([pt[0], pt[1], fixed_z_coords[k]])
        # _fix.append({i + ' fix': _list})

        _save_formatter.add_generic_data(i + "_fix", _list)

    _save_formatter.save_data()

    # with open(os.path.join(path_to_file, file_to_convert), 'w') as f:
    #     json.dump(json_data, f, indent=4)

    print('done?')


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
