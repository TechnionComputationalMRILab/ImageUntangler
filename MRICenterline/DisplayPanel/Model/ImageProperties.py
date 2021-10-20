import math
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.util import numpy_support

import numpy as np

import logging
logging.getLogger(__name__)


class ImageProperties:
    def __init__(self, full_data: vtkImageData, header: dict, window, level, z_coords):
        self.full_data = full_data
        self.spacing = full_data.GetSpacing()
        self.dimensions = full_data.GetDimensions()
        self.extent = full_data.GetExtent()
        self.origin = full_data.GetOrigin()
        self.z_coords = z_coords
        center_z = self.origin[2] + self.spacing[2] * 0.5 * (self.extent[4] + self.extent[5])
        self.sliceIdx = math.ceil((center_z-self.origin[2]) / self.spacing[2])

        # for NNRRD?
        self.dicomArray = numpy_support.vtk_to_numpy(full_data.GetPointData().GetArray(0))
        self.dicomArray = self.dicomArray.reshape(self.dimensions, order='F')

        self.window_value = window
        self.level_value = level

        self.header = header

        min_z = round(center_z - (self.origin[2] + self.spacing[2] * (self.dimensions[2])), 1)
        max_z = math.ceil((self.dimensions[2] * self.spacing[2]) + min_z)

        self.slice_list = dict(zip(np.arange(self.dimensions[2]), z_coords))

    def getParallelScale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])

    def convertZCoordsToSlices(self, z_coords: list):
        _slice_list = []
        for i in z_coords:
            for k, v in self.slice_list.items():
                if round(i, 1) == round(v, 1):
                    _slice_list.append(k)

        return _slice_list
