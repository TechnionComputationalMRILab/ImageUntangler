"""
Testing the shortest path algorithm on case 6, trying to find the bottleneck in the program.
Also useful for debugging the algorithm.
"""

import torch
print(torch.cuda.is_available())

import SimpleITK as sitk
import numpy as np
from MRICenterline.app.shortest_path.find import find_shortest_path

CASE_DIR = r"C:\Users\ang.a\OneDrive - Technion\TCML\Database\ChronsRambam\Initial Batch\Annotated\6"

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(CASE_DIR)
reader.SetFileNames(dicom_names)
image = reader.Execute()

annotation_points = [
    [148, 269, 24],
    [183, 255, 24],
    [183, 255, 23],
    [192, 278, 23],
    [192, 278, 22],
    [267, 375, 22],
    [267, 375, 21],
    [263, 388, 21]
]

import time

print("START")
st = time.time()
shortest_path = find_shortest_path(case_sitk=image, annotation_points=np.array(annotation_points), case_number="6")
et = time.time()
print(f"Time: {et - st}")
print("DONE")
