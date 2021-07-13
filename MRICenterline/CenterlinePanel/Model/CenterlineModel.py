import numpy as np
import vtkmodules.all as vtk
from vtkmodules.all import vtkImageData
from vtkmodules.util import numpy_support

# from icecream import ic

from MRICenterline.CenterlinePanel.Control.CenterlineWidgets import CenterlineWidgets
from MRICenterline.CenterlinePanel.View.CenterlineViewer import CenterlineViewer

from MRICenterline.utils.CalculateCenterline import PointsToPlaneVectors
from MRICenterline.Points.SaveFormatter import SaveFormatter

from MRICenterline.utils import program_constants as CONST
from MRICenterline.Config import ConfigParserRead as CFG
import logging
logging.getLogger(__name__)


class CenterlineModel:
    def __init__(self, image_data, interface):
        self.interface = interface
        self.points = self.interface.get()['points']
        self.image_data = image_data
        self.height = CONST.CL_INITIAL_HEIGHT
        self.angle = CONST.CL_INITIAL_ANGLE

        self.control = CenterlineWidgets(model=self)
        self.view = CenterlineViewer(model=self, control=self.control)

    def set_height(self, height):
        self.height = height

    def set_angle(self, angle):
        self.angle = angle

    def get_mpr_properties(self):
        _mpr_properties = PointsToPlaneVectors(self.points, self.image_data, Plot=0,
                                               height=self.height, viewAngle=self.angle)

        return _mpr_properties

    def calculate_input_data(self):
        _mpr_properties = self.get_mpr_properties()

        _mpr_m = _mpr_properties.MPR_M
        _delta = _mpr_properties.delta
        n = _mpr_m.shape[0]
        m = _mpr_m.shape[1]
        _image_data = vtkImageData()
        _image_data.SetDimensions(n, m, 1)
        _image_data.SetOrigin([0, 0, 0])
        _image_data.SetSpacing([_delta, _delta, _delta])

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

        _image_data.GetPointData().SetScalars(scalars)
        _image_data.Modified()

        logging.info("MPR Calculation")
        return _image_data

    def saveLengths(self, filename, length_points):
        self.control.save_lengths(filename, length_points)
        _save_formatter = SaveFormatter(filename, self.image_data)
        _save_formatter.add_pointcollection_data('length in mpr points', length_points)
        _save_formatter.add_generic_data("mpr points", self.points)
        _save_formatter.save_data()
