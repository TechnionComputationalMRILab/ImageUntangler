#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compare if the origin obtained using the v3 method is the same as the origin obtained in the v4 method

Results: all tests fail
"""

import pydicom
from glob import glob
import numpy as np
import SimpleITK as sitk
import shutil
import tempfile
import pytest

from MRICenterline.testing.test_utils import generate_file_list

cases = generate_file_list()


def generate_v3_sitk_image(folder, reverse=False):
    file_index_list = [(fi, float(pydicom.dcmread(fi)['SliceLocation'].value)) for fi in
                       glob(f'{folder}\\*.dcm')]
    file_index_list.sort(key=lambda x: x[1], reverse=reverse)

    file_list = [fi for fi, _ in file_index_list]

    sitk_image = sitk.ReadImage(file_list)

    origin = sitk_image.GetOrigin()

    return np.array(origin)


def generate_v4_sitk_image(folder):
    reader = sitk.ImageSeriesReader()

    with tempfile.TemporaryDirectory() as temp_dir:
        for fi in glob(f'{folder}\\*.dcm'):
            shutil.copy(src=fi, dst=temp_dir)

        dicom_names = reader.GetGDCMSeriesFileNames(temp_dir)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()

        origin = np.array(image.GetOrigin())

    return origin


@pytest.mark.parametrize('folder', cases)
def test(folder):
    assert generate_v3_sitk_image(folder, reverse=True) == generate_v4_sitk_image(folder)
