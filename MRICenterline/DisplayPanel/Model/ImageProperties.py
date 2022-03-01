import math
import SimpleITK as sitk

import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

import numpy as np

from MRICenterline.Config import CFG
from MRICenterline.utils.TransformationMatrices import transformation_matrix

import logging
logging.getLogger(__name__)


class ImageProperties:
    # def __init__(self, full_data: vtkImageData, header: dict, window, level, z_coords, path):
    def __init__(self, sitk_image):
        self.sitk_image = sitk_image
        self.nparray = sitk.GetArrayFromImage(sitk_image)
        self.spacing = np.array(sitk_image.GetSpacing())
        self.dimensions = np.array(sitk_image.GetDimension())
        self.size = np.array(sitk_image.GetSize())
        self.origin = np.array(sitk_image.GetOrigin())
        self.extent = (0, self.size[0] - 1,
                       0, self.size[1] - 1,
                       0, self.size[2] - 1)

        def calculate_center():
            it = iter(self.extent)
            ext = zip(it, it)

            center = []
            for origin, spacing, (extent_min, extent_max) in zip(self.origin, self.spacing, ext):
                center.append(origin + spacing * 0.5 * (extent_min + extent_max))
            return np.array(center)

        center = calculate_center()
        self.sliceIdx = np.int(np.round(((center[2]-self.origin[2])/self.spacing[2]))) + 1

        self.window_value, self.level_value = self.calculate_window_and_level()

        self.transformation = transformation_matrix(center)

    def __repr__(self):
        return f"""
        ImageProperties instance
        Spacing: {self.spacing}
        Dimensions: {self.dimensions}
        Size: {self.size}
        Origin: {self.origin}
        """

    def calculate_window_and_level(self):
        window_percentile = int(CFG.get_config_data('display', 'window-percentile'))
        window = int(np.percentile(self.nparray, window_percentile))
        level = int(np.percentile(self.nparray, window_percentile) / 2)
        return window, level

    def get_parallel_scale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])

    def get_vtk_data(self):
        vtkVolBase = vtk.vtkImageData()
        vtkVolBase.SetDimensions(*self.size)
        vtkVolBase.SetOrigin(*self.origin)
        vtkVolBase.SetSpacing(*self.spacing)
        vtkVolBase.SetExtent(*self.extent)

        image_array = numpy_support.numpy_to_vtk(self.nparray.ravel(), deep=True, array_type=vtk.VTK_TYPE_UINT16)
        vtkVolBase.GetPointData().SetScalars(image_array)
        vtkVolBase.Modified()

        # return vtkVolBase

        # flip the image in Y direction
        flip = vtk.vtkImageReslice()
        flip.SetInputData(vtkVolBase)
        flip.SetResliceAxesDirectionCosines(1, 0, 0, 0, -1, 0, 0, 0, 1)
        flip.Update()

        vtkVol = flip.GetOutput()
        vtkVol.SetOrigin(*self.origin)

        return vtkVol

    def convert_itk_to_slice(self, itk_z):
        return 1 + self.size[2] - itk_z
