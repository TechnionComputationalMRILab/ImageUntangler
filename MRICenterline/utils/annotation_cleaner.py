from MRICenterline.Loader.LoadPoints import LoadPoints
from MRICenterline.Points.SaveFormatter import SaveFormatter
import numpy as np
import json
import os
from shutil import copy


def convert(imagedata, bad_z_coords):
    print("CONVERTING")

    fixed_z_coords = imagedata.z_coords
    path_to_file = 'C:\\Users\\ang.a\\OneDrive - Technion\\Documents\\MRI_Data\\problematic_enc_files\\104\\data'
    file_list = ['17.10.2021__12_34..annotation.json', '17.10.2021__12_33..annotation.json', '17.10.2021__12_32..annotation.json']

    for file_to_convert in file_list:
        copy(os.path.join(path_to_file, file_to_convert), os.path.join(path_to_file, "BACKUP__" + file_to_convert))
        lp = LoadPoints(os.path.join(path_to_file, file_to_convert), imagedata, get_raw_dataset=True)

        # for i in lp.point_set.values():
        #     for pt in i:
        #         for k, bad_z in enumerate(bad_z_coords):
        #             if np.isclose(pt[2], bad_z):
        #                 pass
                        # print(f"replace {bad_z} with {fixed_z_coords[k]}")

        with open(os.path.join(path_to_file, file_to_convert), 'r') as f:
            json_data = json.load(f)

        for i in lp.point_set.keys():
            print(i)
            for pt in json_data[i]:
                for k, bad_z in enumerate(bad_z_coords):
                    if np.isclose(pt[2], bad_z):
                        print(f"replace {bad_z} with {fixed_z_coords[k]}")
                        pt[2] = fixed_z_coords[k]

        _save_formatter = SaveFormatter(imagedata, append_to_directory=False)
        for i in lp.point_set.keys():
            _save_formatter.add_generic_data(i, json_data[i])

        # with open(os.path.join(path_to_file, file_to_convert), 'w') as f:
        #     json.dump(json_data, f, indent=4)

        print('done?')


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
