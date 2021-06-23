import vtkmodules.all as vtk
import numpy as np
from vtk.util import numpy_support


def numpy_array_as_vtk_image_data(source_numpy_array):
    """
    :param source_numpy_array: source array with 2-3 dimensions. If used, the third dimension represents the channel count.
    Note: Channels are flipped, i.e. source is assumed to be BGR instead of RGB (which works if you're using cv2.imread function to read three-channel images)
    Note: Assumes array value at [0,0] represents the upper-left pixel.
    :type source_numpy_array: np.ndarray
    :return: vtk-compatible image, if conversion is successful. Raises exception otherwise
    :rtype vtk.vtkImageData

    source: https://stackoverflow.com/a/61563445
    """

    if len(source_numpy_array.shape) > 2:
        channel_count = source_numpy_array.shape[2]
    else:
        channel_count = 1

    output_vtk_image = vtk.vtkImageData()
    output_vtk_image.SetDimensions(source_numpy_array.shape[1], source_numpy_array.shape[0], channel_count)

    vtk_type_by_numpy_type = {
        np.uint8: vtk.VTK_UNSIGNED_CHAR,
        np.uint16: vtk.VTK_UNSIGNED_SHORT,
        np.uint32: vtk.VTK_UNSIGNED_INT,
        np.uint64: vtk.VTK_UNSIGNED_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_UNSIGNED_LONG_LONG,
        np.int8: vtk.VTK_CHAR,
        np.int16: vtk.VTK_SHORT,
        np.int32: vtk.VTK_INT,
        np.int64: vtk.VTK_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_LONG_LONG,
        np.float32: vtk.VTK_FLOAT,
        np.float64: vtk.VTK_DOUBLE
    }
    vtk_datatype = vtk_type_by_numpy_type[source_numpy_array.dtype.type]

    source_numpy_array = np.flipud(source_numpy_array)

    # Note: don't flip (take out next two lines) if input is RGB.
    # Likewise, BGRA->RGBA would require a different reordering here.
    if channel_count > 1:
        source_numpy_array = np.flip(source_numpy_array, 2)

    depth_array = numpy_support.numpy_to_vtk(source_numpy_array.ravel(), deep=True, array_type = vtk_datatype)
    depth_array.SetNumberOfComponents(channel_count)
    output_vtk_image.SetSpacing([1, 1, 1])
    output_vtk_image.SetOrigin([-1, -1, -1])
    output_vtk_image.GetPointData().SetScalars(depth_array)

    output_vtk_image.Modified()
    return output_vtk_image
