import math

import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

from SimpleITK import GetArrayFromImage
import numpy as np

from MRICenterline import CFG
from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
from MRICenterline.app.file_reader.dicom.DICOMReader import DICOMReader
from MRICenterline.app.file_reader.imager import Imager
from MRICenterline.app.file_reader.transformation_matrix import transformation_matrix

import logging
logging.getLogger(__name__)


class ImageProperties:
    def __init__(self, sitk_image, image_orientation: ImageOrientation, z_coords):
        self.sitk_image = sitk_image
        self.orientation = image_orientation

        self.spacing = np.array(sitk_image.GetSpacing())
        self.dimensions = np.int32(sitk_image.GetDimension())
        self.size = np.array(sitk_image.GetSize())
        self.origin = np.array(sitk_image.GetOrigin())

        self.extent = [i for j in [[0, self.size[k] - 1] for k in range(self.dimensions)] for i in j]

        self.nparray = GetArrayFromImage(sitk_image)
        self.data = self.nparray

        def calculate_center():
            it = iter(self.extent)
            ext = zip(it, it)

            center = []
            for origin, spacing, (extent_min, extent_max) in zip(self.origin, self.spacing, ext):
                calculated_center = origin + spacing * 0.5 * (extent_min + extent_max)
                center.append(round(calculated_center, 1))
            return np.array(center)

        center = calculate_center()
        # changed to -1 from 2 to handle 2D cases. might be problematic??
        self.sliceIdx = np.int(np.round(((center[-1]-self.origin[-1])/self.spacing[-1]))) + 1

        self.vtk_data = self.get_vtk_data()
        self.transformation = transformation_matrix(center, view='y_flip_axial')

        self.direction_matrix = sitk_image.GetDirection()

        self.window_value, self.level_value = self.calculate_window_and_level()
        self.z_coords = z_coords

    def __repr__(self):
        return f"""
        ImageProperties instance
        Spacing: {self.spacing}
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

    def convert_itk_to_slice(self, itk_z):
        return 1 + self.size[2] - itk_z

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
        # flip.SetResliceAxesDirectionCosines(1, 0, 0, 0, -1, 0, 0, 0, 1)
        flip.Update()

        vtkVol = flip.GetOutput()
        vtkVol.SetOrigin(*self.origin)

        return vtkVol

    @classmethod
    def from_path(cls, folder, seq_id):
        imager = Imager(folder)

        if isinstance(imager.reader, DICOMReader):
            idx = imager.reader.find_index_from_seq_id(seq_id=seq_id)
            sitk_image = imager.reader[idx]
            orientation = imager.reader.get_image_orientation(idx)

            return cls(sitk_image, orientation, [])
