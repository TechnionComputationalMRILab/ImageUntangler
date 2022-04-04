from vtkmodules.all import VTK_UNSIGNED_CHAR, VTK_UNSIGNED_SHORT, VTK_UNSIGNED_INT, VTK_UNSIGNED_LONG, \
    VTK_UNSIGNED_LONG_LONG, VTK_CHAR, VTK_SHORT, VTK_INT, VTK_LONG, VTK_SIZEOF_LONG,\
    VTK_LONG_LONG, VTK_FLOAT, VTK_DOUBLE
import numpy as np
from vtkmodules.all import vtkImageData
from vtkmodules.util import numpy_support


def vtk_transform(mpr_properties):
    mpr_m = mpr_properties.MPR_M
    delta = mpr_properties.delta

    n = mpr_m.shape[0]
    m = mpr_m.shape[1]

    image_data = vtkImageData()
    image_data.SetDimensions(n, m, 1)
    image_data.SetOrigin(0, 0, 0)
    image_data.SetSpacing(delta, delta, delta)

    vtk_type_by_numpy_type = {
        np.uint8: VTK_UNSIGNED_CHAR,
        np.uint16: VTK_UNSIGNED_SHORT,
        np.uint32: VTK_UNSIGNED_INT,
        np.uint64: VTK_UNSIGNED_LONG if VTK_SIZEOF_LONG == 64 else VTK_UNSIGNED_LONG_LONG,
        np.int8: VTK_CHAR,
        np.int16: VTK_SHORT,
        np.int32: VTK_INT,
        np.int64: VTK_LONG if VTK_SIZEOF_LONG == 64 else VTK_LONG_LONG,
        np.float32: VTK_FLOAT,
        np.float64: VTK_DOUBLE
    }

    vtk_datatype = vtk_type_by_numpy_type[mpr_m.dtype.type]
    mpr_m = np.transpose(mpr_m)
    scalars = numpy_support.numpy_to_vtk(num_array=mpr_m.ravel(), deep=True, array_type=vtk_datatype)

    image_data.GetPointData().SetScalars(scalars)
    image_data.Modified()

    return image_data
