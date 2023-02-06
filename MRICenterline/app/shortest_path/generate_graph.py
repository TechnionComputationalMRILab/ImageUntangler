import numpy as np
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[3]))

import SimpleITK as sitk
from MRICenterline.app.shortest_path.functions import calc_graph_weights
from MRICenterline.app.shortest_path.find import GRID_PIXELS_SIZE, PATCH_LEN
from MRICenterline import CFG

sitk_image_path = r"C:\Users\ang.a\OneDrive - Technion\TCML\Database\ChronsRambam\Initial Batch\Annotated\6"
saved_graph_path = r'C:\Users\ang.a\Documents\TCML-repos\ImageUntangler\MRICenterline\app\shortest_path\saved_graph'

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(sitk_image_path)
reader.SetFileNames(dicom_names)
image: sitk.Image = reader.Execute()

case_number = 6
# slice_num = 13
x_len, y_len, max_slice = image.GetSize()

if not CFG.torch_cuda_available:
    assert False, "CUDA required"
else:
    for slice_num in range(17, 27):
        print("Processing", slice_num)
        graph_weights = calc_graph_weights(0, 0, x_len*y_len, x_len, y_len,
                                           slice_num, image, PATCH_LEN, GRID_PIXELS_SIZE, case_number)

        np.save(os.path.join(saved_graph_path, "6", f"{slice_num}.npy"), graph_weights)

# slice_dict = {}
# for i in range(max_slice):
#     slice_dict[i] = graph_weights...
# np.savez(filename, **slice_dict)
