from vtkmodules.all import VTK_UNSIGNED_CHAR, VTK_UNSIGNED_SHORT, VTK_UNSIGNED_INT, VTK_UNSIGNED_LONG, \
    VTK_UNSIGNED_LONG_LONG, VTK_CHAR, VTK_SHORT, VTK_INT, VTK_LONG, VTK_SIZEOF_LONG,\
    VTK_LONG_LONG, VTK_FLOAT, VTK_DOUBLE
import numpy as np
from vtkmodules.all import vtkImageData
from vtkmodules.util import numpy_support

from MRICenterline.app.centerline.calculate import PointsToPlaneVectors


class CenterlineModel:
    def __init__(self, case_model):
        self.case_model = case_model
        self.widget = None
        self.point_array = None
        self.image_properties = None
        self.centerline_viewer = None
        self.parallel_scale = 0.1

        self.vtk_data = vtkImageData()

    def set_points_and_image(self, points, image):
        self.point_array = points
        self.image_properties = image

    def connect_viewer(self, centerline_viewer):
        self.centerline_viewer = centerline_viewer

    def connect_widget(self, widget):
        self.widget = widget

    def update_widget(self):
        self.widget.label.setText(f"Calculating MPR on {len(self.point_array)}")

        self.calculate_centerline()
        self.centerline_viewer.refresh_panel()

    def calculate_centerline(self):
        ppv = PointsToPlaneVectors(self.point_array.get_as_np_array(),
                                   self.image_properties)

        _mpr_m = ppv.MPR_M
        _delta = ppv.delta

        n = _mpr_m.shape[0]
        m = _mpr_m.shape[1]

        self.vtk_data.SetDimensions(n, m, 1)
        self.vtk_data.SetOrigin(0, 0, 0)
        self.vtk_data.SetSpacing(_delta, _delta, _delta)

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

        self.vtk_data.GetPointData().SetScalars(scalars)
        self.vtk_data.Modified()

        self.parallel_scale = self.parallel_scale * _delta * (self.vtk_data.GetExtent()[1] - self.vtk_data.GetExtent()[0])
