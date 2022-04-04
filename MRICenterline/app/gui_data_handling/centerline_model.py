from vtkmodules.all import vtkImageData

from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.centerline.calculate import PointsToPlaneVectors
from MRICenterline.gui.vtk.transform_to_vtk import vtk_transform

from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray

from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class CenterlineModel:
    picker_status = PickerStatus.NOT_PICKING

    def __init__(self, case_model):
        self.case_model = case_model
        self.window_value, self.level_value = self.case_model.window_value, self.case_model.level_value
        self.widget = None
        self.point_array = None
        self.image_properties = None
        self.centerline_viewer = None
        self.parallel_scale = 0.1
        self.length_point_array = PointArray(PointStatus.LENGTH_IN_MPR)

        self.height = 30
        self.angle = 0

        self.vtk_data = vtkImageData()

    def set_window_level(self, wval, lval):
        self.window_value = wval
        self.level_value = lval
        self.centerline_viewer.set_window_level()

    def set_points_and_image(self, points, image):
        self.point_array = points
        self.image_properties = image

    def connect_viewer(self, centerline_viewer):
        self.centerline_viewer = centerline_viewer

    def connect_widget(self, widget):
        self.widget = widget

    def update_widget(self):
        self.widget.label.setText(f"Calculating MPR on {len(self.point_array)} points")

        self.calculate_centerline()
        self.centerline_viewer.initialize_panel()

    def save(self):
        print("save points")

    def refresh_panel(self, angle_change=None, height_change=None):
        self.calculate_centerline()
        self.centerline_viewer.refresh_panel(angle_change, height_change)

    def pick(self, pick_coords):
        point = Point(pick_coords, 0, None)

        if self.picker_status == PickerStatus.PICKING_LENGTH:
            self.length_point_array.add_point(point)
            self.centerline_viewer.add_actor(self.length_point_array.get_last_actor())

            if CFG.get_boolean('mpr-length-display-style', 'show-line') and len(self.length_point_array) >= 2:
                self.centerline_viewer.add_actor(self.length_point_array.get_last_line_actor())

    def calculate_length(self):
        if len(self.length_point_array) >= 2:
            print(self.length_point_array.lengths)
            print(self.length_point_array.total_length)

    def set_picker_status(self, status: PickerStatus):
        logging.debug(f"Setting centerline panel picker status to {status}")
        self.picker_status = status

    def adjust_height(self, delta_h):
        self.height += delta_h

        logging.debug(f"Adjusting height to {self.height}")
        self.refresh_panel(height_change=self.height)

    def adjust_angle(self, delta_a):
        if (self.angle + delta_a) > 180:
            self.angle = 0
        elif (self.angle + delta_a) < 0:
            self.angle = 180
        else:
            self.angle += delta_a

        logging.debug(f"Adjusting angle to {self.angle}")
        self.refresh_panel(angle_change=self.angle)

    def calculate_centerline(self):
        input_points = self.point_array.get_as_np_array()

        input_points = [
        [
            -76.14312065972223,
            -2.0789930555555647,
            -29.820188894288
        ],
        [
            -76.92274305555554,
            -5.457356770833338,
            -29.820188894288
        ],
        [
            -78.48198784722223,
            -8.056098090277782,
            -29.820188894288
        ],
        [
            -79.78135850694446,
            -11.174587673611104,
            -29.820188894288
        ],
        [
            -80.82085503472224,
            -14.29307725694445,
            -29.820188894288
        ],
        [
            -82.12022569444447,
            -16.37207031249999,
            -34.820187069056
        ],
        [
            -82.63997395833333,
            -20.010308159722214,
            -34.820187069056
        ],
        [
            -83.15972222222224,
            -22.609049479166657,
            -34.820187069056
        ],
        [
            -84.19921875000001,
            -26.247287326388882,
            -34.820187069056
        ],
        [
            -84.19921875000001,
            -28.32628038194445,
            -39.820189057903
        ],
        [
            -84.45909288194447,
            -30.925021701388893,
            -39.820189057903
        ],
        [
            -84.97884114583333,
            -34.043511284722214,
            -39.820189057903
        ],
        [
            -86.0183376736111,
            -35.86263020833333,
            -44.820187232604
        ],
        [
            -86.0183376736111,
            -38.46137152777777,
            -44.820187232604
        ],
        [
            -85.75846354166664,
            -40.80023871527776,
            -44.820187232604
        ],
        [
            -84.71896701388887,
            -43.65885416666666,
            -44.820187232604
        ],
        [
            -86.0183376736111,
            -44.698350694444436,
            -49.820189221517
        ],
        [
            -86.0183376736111,
            -47.556966145833336,
            -49.820189221517
        ],
        [
            -85.23871527777779,
            -49.89583333333332,
            -49.820189221517
        ],
        [
            -85.23871527777779,
            -52.75444878472222,
            -49.820189221517
        ],
        [
            -84.45909288194447,
            -55.09331597222221,
            -49.820189221517
        ],
        [
            -83.6794704861111,
            -57.17230902777778,
            -49.820189221517
        ],
        [
            -83.4195963541667,
            -58.991427951388886,
            -54.820187396285
        ],
        [
            -82.12022569444447,
            -62.10991753472221,
            -54.820187396285
        ],
        [
            -81.3406032986111,
            -64.44878472222223,
            -54.820187396285
        ],
        [
            -83.93934461805556,
            -67.3074001736111,
            -59.820189385131
        ],
        [
            -83.4195963541667,
            -69.90614149305554,
            -59.820189385131
        ],
        [
            -82.63997395833333,
            -71.9851345486111,
            -59.820189385131
        ],
        [
            -84.97884114583333,
            -71.9851345486111,
            -64.820191373978
        ],
        [
            -83.4195963541667,
            -74.58387586805554,
            -64.820191373978
        ],
        [
            -83.93934461805556,
            -74.58387586805554,
            -69.820185734667
        ],
        [
            -82.38009982638887,
            -75.36349826388887,
            -69.820185734667
        ],
        [
            -80.30110677083333,
            -77.44249131944444,
            -69.820185734667
        ],
        [
            -79.78135850694446,
            -79.78135850694443,
            -69.820185734667
        ],
        [
            -79.00173611111109,
            -83.1597222222222,
            -69.820185734667
        ],
        [
            -78.22211371527777,
            -85.75846354166666,
            -69.820185734667
        ],
        [
            -77.1826171875,
            -88.09733072916667,
            -69.820185734667
        ],
        [
            -76.40299479166669,
            -90.43619791666666,
            -69.820185734667
        ],
        [
            -76.40299479166669,
            -91.99544270833331,
            -69.820185734667
        ],
        [
            -75.10362413194446,
            -94.33430989583331,
            -69.820185734667
        ],
        [
            -74.32400173611114,
            -97.71267361111111,
            -69.820185734667
        ],
        [
            -74.32400173611114,
            -97.71267361111111,
            -74.820187723513
        ],
        [
            -73.02463107638891,
            -100.0515407986111,
            -74.820187723513
        ],
        [
            -72.5048828125,
            -102.91015625,
            -74.820187723513
        ],
        [
            -71.98513454861114,
            -106.28851996527777,
            -74.820187723513
        ],
        [
            -70.94563802083331,
            -108.36751302083331,
            -74.820187723513
        ],
        [
            -69.64626736111113,
            -110.70638020833333,
            -74.820187723513
        ],
        [
            -68.3468967013889,
            -113.04524739583331,
            -74.820187723513
        ],
        [
            -66.26790364583336,
            -113.82486979166664,
            -74.820187723513
        ],
        [
            -64.18891059027776,
            -114.86436631944443,
            -74.820187723513
        ],
        [
            -61.85004340277781,
            -115.38411458333331,
            -74.820187723513
        ],
        [
            -58.21180555555557,
            -116.42361111111111,
            -74.820187723513
        ],
        [
            -55.613064236111114,
            -117.98285590277777,
            -74.820187723513
        ],
        [
            -52.49457465277779,
            -119.54210069444444,
            -74.820187723513
        ],
        [
            -49.895833333333336,
            -121.62109375,
            -74.820187723513
        ],
        [
            -48.85633680555556,
            -124.47970920138887,
            -74.820187723513
        ],
        [
            -47.29709201388887,
            -127.5981987847222,
            -74.820187723513
        ],
        [
            -46.777343750000014,
            -130.71668836805554,
            -74.820187723513
        ]
    ]

        ppv = PointsToPlaneVectors(input_points,
                                   self.image_properties,
                                   height=self.height,
                                   angle_degrees=self.angle)

        self.vtk_data = vtk_transform(ppv)
        self.parallel_scale = self.parallel_scale * ppv.delta * \
                              (self.vtk_data.GetExtent()[1] - self.vtk_data.GetExtent()[0])
