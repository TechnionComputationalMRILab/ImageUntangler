import vtkmodules.all as vtk
from MPRwindow import MPRInteractor
from util import stylesheets
import numpy as np
from vtk import vtkImageData
from vtk.util import numpy_support
from Model import getMPR
from Model.PointCollection import PointCollection
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# from MPRWindow2.MPRW_View import MPRW_View


class MPRW_Model:
    def __init__(self, control):
        self.control = control

    def set_angle(self, angle):
        self.control.set_angle(angle)

    def set_height(self, height):
        self.control.set_angle(height)

    def get_angle(self):
        return self.control.viewAngle

    def get_height(self):
        return self.control.height

    def calculate_input_data(self):
        _mpr_properties = self.control.calculate()

        _mpr_m = _mpr_properties.MPR_M
        _delta = _mpr_properties.delta
        n = _mpr_m.shape[0]
        m = _mpr_m.shape[1]
        _mpr_vtk = vtkImageData()
        _mpr_vtk.SetDimensions(n, m, 1)
        _mpr_vtk.SetOrigin([0, 0, 0])
        _mpr_vtk.SetSpacing([_delta, _delta, _delta])

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

        vtk_datatype = vtk_type_by_numpy_type[_mpr_m.dtype.type]
        _mpr_m = np.transpose(_mpr_m)
        scalars = numpy_support.numpy_to_vtk(num_array=_mpr_m.ravel(), deep=True, array_type=vtk_datatype)

        _mpr_vtk.GetPointData().SetScalars(scalars)
        _mpr_vtk.Modified()

        return _mpr_vtk
