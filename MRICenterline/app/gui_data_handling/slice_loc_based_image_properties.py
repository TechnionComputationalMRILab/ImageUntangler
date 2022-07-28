import math
import numpy as np

import SimpleITK as sitk
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties

import logging
logging.getLogger(__name__)


class SliceLocImageProperties(ImageProperties):
    def __init__(self, np_array, image_orientation, z_coords, file_list, parent=None):

        sitk_image = sitk.ReadImage(file_list)

        super().__init__(sitk_image=sitk_image, image_orientation=image_orientation, parent=parent)

        self.vtk_data = self.get_vtk_data_old(np_arr=np_array,
                                              origin=sitk_image.GetOrigin(),
                                              spacing=sitk_image.GetSpacing(),
                                              ncomp=sitk_image.GetNumberOfComponentsPerPixel(),
                                              direction=sitk_image.GetDirection(),
                                              size=sitk_image.GetSize())

        self.size = sitk_image.GetSize()
        self.spacing = self.vtk_data.GetSpacing()
        self.dimensions = self.vtk_data.GetDimensions()
        self.extent = self.vtk_data.GetExtent()
        self.origin = self.vtk_data.GetOrigin()

        center_z = self.origin[2] + self.spacing[2] * 0.5 * (self.extent[4] + self.extent[5])
        self.sliceIdx = math.ceil((center_z-self.origin[2]) / self.spacing[2])

        self.nparray = numpy_support.vtk_to_numpy(self.vtk_data.GetPointData().GetArray(0))
        self.nparray = self.nparray.reshape(self.dimensions, order='F')

        self.z_coords = sorted(list(set(z_coords)))

        x0, y0, z0 = self.origin
        x_spacing, y_spacing, z_spacing = self.spacing
        x_min, x_max, y_min, y_max, z_min, z_max = self.extent

        center = [x0 + x_spacing * 0.5 * (x_min + x_max),
                       y0 + y_spacing * 0.5 * (y_min + y_max),
                       z0 + z_spacing * 0.5 * (z_min + z_max)]

        self.transformation = vtk.vtkMatrix4x4()
        self.transformation.DeepCopy((1, 0, 0, center[0],
                             0, -1, 0, center[1],
                             0, 0, 1, center[2],
                             0, 0, 0, 1))

    @staticmethod
    def get_vtk_data_old(np_arr, origin, spacing, ncomp, direction, size):
        """ adapted from https://github.com/dave3d/dicom2stl/blob/main/utils/sitk2vtk.py """

        np_arr = np.flipud(np_arr)
        vtk_image = vtk.vtkImageData()

        size = list(size)
        origin = list(origin)
        spacing = list(spacing)

        # VTK expects 3-dimensional parameters
        if len(size) == 2:
            size.append(1)

        if len(origin) == 2:
            origin.append(0.0)

        if len(spacing) == 2:
            spacing.append(spacing[0])

        # if len(direction) == 4:
        #     direction = [ direction[0], direction[1], 0.0,
        #                   direction[2], direction[3], 0.0,
        #                            0.0,          0.0, 1.0 ]

        vtk_image.SetDimensions(size)
        vtk_image.SetSpacing(spacing)
        vtk_image.SetOrigin(origin)
        vtk_image.SetExtent(0, size[0] - 1, 0, size[1] - 1, 0, size[2] - 1)

        # if vtk.vtkVersion.GetVTKMajorVersion()<9:
        #     print("Warning: VTK version <9.  No direction matrix.")
        # else:
        #     vtk_image.SetDirectionMatrix(direction)

        # depth_array = numpy_support.numpy_to_vtk(i2.ravel(), deep=True,
        #                                          array_type = vtktype)
        depth_array = numpy_support.numpy_to_vtk(np_arr.ravel())
        depth_array.SetNumberOfComponents(ncomp)
        vtk_image.GetPointData().SetScalars(depth_array)

        vtk_image.Modified()

        # print(f"VTK Direction Matrix: \n {vtk_image.GetDirectionMatrix()}")

        return vtk_image
