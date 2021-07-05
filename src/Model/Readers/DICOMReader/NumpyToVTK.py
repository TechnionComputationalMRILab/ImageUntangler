import vtkmodules.all as vtk
import numpy as np
from vtkmodules.util import numpy_support

debugOn = False


def numpy_array_as_vtk_image_data(np_arr, origin, spacing):
    """
    source: adapted from https://github.com/dave3d/dicom2stl/blob/main/utils/sitk2vtk.py
    """
    np_arr = np.flipud(np_arr)  # either this, or reshape with order F? TODO: check this
    vtk_image = vtk.vtkImageData()

    size = list(np_arr.shape)
    origin = list(origin)
    spacing = list(spacing) # get this from PixelSpacing in the header

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
    depth_array.SetNumberOfComponents(2)
    vtk_image.GetPointData().SetScalars(depth_array)

    vtk_image.Modified()
    #
    if debugOn:
        print("Volume object inside sitk2vtk")
        # print(vtk_image)
        print(size)
        print(origin)
        print(spacing)
        # print(vtk_image.GetScalarComponentAsFloat(0, 0, 0, 0))

    return vtk_image