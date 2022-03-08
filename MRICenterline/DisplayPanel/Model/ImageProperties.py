import math

import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

import numpy as np

from MRICenterline.Config import CFG
from MRICenterline.utils.TransformationMatrices import transformation_matrix

import logging
logging.getLogger(__name__)


class ImageProperties:
    def __init__(self, full_data: vtk.vtkImageData, np_array):
        self.full_data = full_data
        self.spacing = full_data.GetSpacing()
        self.dimensions = full_data.GetDimensions()
        self.extent = full_data.GetExtent()
        self.origin = full_data.GetOrigin()
        self.size = full_data.GetDimensions()

        def calculate_center():
            it = iter(self.extent)
            ext = zip(it, it)

            center = []
            for origin, spacing, (extent_min, extent_max) in zip(self.origin, self.spacing, ext):
                center.append(origin + spacing * 0.5 * (extent_min + extent_max))
            return np.array(center)

        center = calculate_center()
        self.sliceIdx = np.int(np.round(((center[2]-self.origin[2])/self.spacing[2]))) + 1

        # self.nparray = numpy_support.vtk_to_numpy(full_data.GetPointData().GetArray(0))
        self.nparray = np_array
        self.nparray = self.nparray.reshape(self.dimensions, order='F')

        self.window_value, self.level_value = self.calculate_window_and_level()
        self.transformation = transformation_matrix(center)

    def __repr__(self):
        return f"""
        ImageProperties instance
        Spacing: {self.spacing}
        Dimensions: {self.dimensions}
        Origin: {self.origin}
        """

    def calculate_window_and_level(self):
        window_percentile = int(CFG.get_config_data('display', 'window-percentile'))
        window = int(np.percentile(self.nparray, window_percentile))
        level = int(np.percentile(self.nparray, window_percentile) / 2)
        return window, level

    def get_parallel_scale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])

    def convert_itk_to_slice(self, itk_z):
        return 1 + self.dimensions[2] - itk_z
