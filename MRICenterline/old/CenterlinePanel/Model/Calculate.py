from vtkmodules.all import VTK_UNSIGNED_CHAR, VTK_UNSIGNED_SHORT, VTK_UNSIGNED_INT, VTK_UNSIGNED_LONG, \
    VTK_UNSIGNED_LONG_LONG, VTK_CHAR, VTK_SHORT, VTK_INT, VTK_LONG, VTK_SIZEOF_LONG,\
    VTK_LONG_LONG, VTK_FLOAT, VTK_DOUBLE
import numpy as np
from vtkmodules.all import vtkImageData
from vtkmodules.util import numpy_support


def calculate_input_data(mpr_properties):
    _mpr_m = mpr_properties.MPR_M
    _delta = mpr_properties.delta

    n = _mpr_m.shape[0]
    m = _mpr_m.shape[1]

    _image_data = vtkImageData()
    _image_data.SetDimensions(n, m, 1)
    _image_data.SetOrigin(0, 0, 0)
    _image_data.SetSpacing(_delta, _delta, _delta)

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

    vtk_datatype = vtk_type_by_numpy_type[_mpr_m.dtype.type]
    _mpr_m = np.transpose(_mpr_m)
    scalars = numpy_support.numpy_to_vtk(num_array=_mpr_m.ravel(), deep=True, array_type=vtk_datatype)

    _image_data.GetPointData().SetScalars(scalars)
    _image_data.Modified()

    return _image_data
