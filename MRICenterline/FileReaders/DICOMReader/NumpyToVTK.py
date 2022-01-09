from vtkmodules.all import vtkImageData
import numpy as np
from vtkmodules.util import numpy_support
from SimpleITK import ReadImage, ProcessObject_SetGlobalWarningDisplay

ProcessObject_SetGlobalWarningDisplay(False)

import logging
logging.getLogger(__name__)

NP_TO_VTK_DEBUG = False


def get_image_properties(file_list):
    _prop = dict()

    dicom_itk = ReadImage(file_list)

    _prop['size'] = list(dicom_itk.GetSize())
    _prop['origin'] = list(dicom_itk.GetOrigin())
    _prop['spacing'] = list(dicom_itk.GetSpacing())
    _prop['ncomp'] = dicom_itk.GetNumberOfComponentsPerPixel()
    _prop['direction'] = dicom_itk.GetDirection()

    return _prop, dicom_itk


def numpy_array_as_vtk_image_data(np_arr, origin, spacing, ncomp, direction, size):
    """ adapted from https://github.com/dave3d/dicom2stl/blob/main/utils/sitk2vtk.py """
    np_arr = np.flipud(np_arr)  # sITK reads image data differently. this is how to fix it
    vtk_image = vtkImageData()

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
    # direction = [ 1.0,  0.0,  0.0,
    #               0.0,  0.0,  1.0,
    #               0.0, -1.0,  0.0]
    vtk_image.SetDirectionMatrix(direction)

    vtk_image.SetDimensions(*size)
    vtk_image.SetSpacing(*spacing)
    vtk_image.SetOrigin(*origin)
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

    if NP_TO_VTK_DEBUG:
        print("Volume object inside sitk2vtk")
        # print(vtk_image)
        print(size)
        print(origin)
        print(spacing)
        # print(vtk_image.GetScalarComponentAsFloat(0, 0, 0, 0))

    return vtk_image
