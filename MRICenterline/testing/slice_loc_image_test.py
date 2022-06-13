#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
compares the output of the v3 method of generating the image that reads each
DICOM file on its own and the v4 method that uses sitk directly
"""

import os

import numpy as np
from PyQt5 import QtCore
from PyQt5.Qt import *
import pytest

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget

PATH_FOR_TEST_CASES = r'C:\Users\ang.a\Database\Rambam\clean_cases'
cases = [os.path.join(PATH_FOR_TEST_CASES, name)
         for name in os.listdir(PATH_FOR_TEST_CASES)
         if os.path.isdir(os.path.join(PATH_FOR_TEST_CASES, name))]


def generate_v4_image(folder):
    import SimpleITK as sitk
    import shutil
    import tempfile
    from glob import glob

    reader = sitk.ImageSeriesReader()

    with tempfile.TemporaryDirectory() as temp_dir:
        for fi in glob(f'{folder}\\*.dcm'):
            shutil.copy(src=fi, dst=temp_dir)

        dicom_names = reader.GetGDCMSeriesFileNames(temp_dir)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()

    return image


@pytest.mark.parametrize('folder', cases)
def test(qtbot, folder):
    case_model = CaseModel(folder)
    widget = MainDisplayWidget(case_model)
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton)

    current_np_image = case_model.sequence_manager.current_image_properties.nparray
    v4_sitk_image = generate_v4_image(folder)
    v4_np = np.zeros_like(current_np_image)

    for i in range(current_np_image.shape[0]):
        for j in range(current_np_image.shape[1]):
            for k in range(current_np_image.shape[2]):
                v4_np[i, j, k] = v4_sitk_image.GetPixel(i, j, k)

    assert np.allclose(current_np_image, v4_np)
