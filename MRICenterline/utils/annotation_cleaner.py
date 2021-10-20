from MRICenterline.Loader.LoadPoints import LoadPoints
import numpy as np
import json


def convert(imagedata, bad_z_coords):
    print(bad_z_coords)
    fixed_z_coords = imagedata.z_coords
    file_to_convert = 'C:\\Users\\ang.a\\OneDrive - Technion\\Documents\\MRI_Data\\problematic_enc_files\\107\\data\\20.10.2021__09_37..annotation.json'

    lp = LoadPoints(file_to_convert, imagedata, get_raw_dataset=True)

    # for i in lp.point_set.values():
    #     for pt in i:
    #         for k, bad_z in enumerate(bad_z_coords):
    #             if np.isclose(pt[2], bad_z):
    #                 pass
                    # print(f"replace {bad_z} with {fixed_z_coords[k]}")

    with open(file_to_convert, 'r') as f:
        json_data = json.load(f)

    for i in lp.point_set.keys():
        print(i)
        for pt in json_data[i]:
            for k, bad_z in enumerate(bad_z_coords):
                if np.isclose(pt[2], bad_z):
                    print(f"replace {bad_z} with {fixed_z_coords[k]}")
                    pt[2] = fixed_z_coords[k]

    with open(file_to_convert, 'w') as f:
        json.dump(json_data, f, indent=4)

    print('done?')

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
