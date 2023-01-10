from vtkmodules.all import vtkImageData

from MRICenterline.app.gui_data_handling.centerline_image_properties import CenterlineImageProperties
from MRICenterline.app.points.point2d import Point2D
from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.centerline.calculate import get_straight_mpr
from MRICenterline.gui.vtk.transform_to_vtk import vtk_transform

from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.gui.vtk.line_actor import VerticalLine, VerticalLineArray

from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


class CenterlineModel:
    picker_status = PickerStatus.NOT_PICKING

    def __init__(self, case_model):
        self.parallel_scale = 1
        self.case_model = case_model
        self.window_value, self.level_value = self.case_model.window_value, self.case_model.level_value
        self.widget = None
        self.point_array = None
        self.original_image_properties = None
        self.cl_image_properties = None
        self.centerline_viewer = None
        self.length_point_array = PointArray(PointStatus.LENGTH_IN_MPR)

        self.height = 30
        self.angle = 0

        self.vtk_data = vtkImageData()
        self.nparray = None
        self.point_markers = VerticalLineArray()

        self.has_highlight = False
        self.previous_mouse_coords = None
        self.two_points_set = False

    def set_window_level(self, wval, lval):
        self.window_value = wval
        self.level_value = lval
        self.centerline_viewer.set_window_level()

    def set_points_and_image(self, points, image):
        self.point_array = points
        self.original_image_properties = image

    def connect_viewer(self, centerline_viewer):
        self.centerline_viewer = centerline_viewer

    def connect_widget(self, widget):
        self.widget = widget

    def update_widget(self):
        self.widget.label.setText(f"Calculating MPR on {len(self.point_array)} points")

        self.calculate_centerline()
        self.centerline_viewer.initialize_panel()

    def save(self):
        # TODO: save measurements from centerline calculations
        print("save points")

    def export(self, destination, export_options):
        from MRICenterline.app.export.centerline import export
        export(self, destination, export_options)

    def refresh_panel(self, angle_change=None, height_change=None):
        self.calculate_centerline()
        self.centerline_viewer.refresh_panel(angle_change, height_change)

    def pick(self, pick_coords):
        point = Point2D(pick_coords, self.cl_image_properties)

        if self.picker_status == PickerStatus.PICKING_LENGTH:

            if len(self.length_point_array) < 2:
                self.length_point_array.add_point(point)
                self.centerline_viewer.add_actor(self.length_point_array.get_last_actor())

                if CFG.get_boolean('mpr-length-display-style', 'show-line') and len(self.length_point_array) >= 2:
                    self.centerline_viewer.add_actor(self.length_point_array.get_last_line_actor())
            else:
                print("adding extra point")
                self.length_point_array.clear()
                self.centerline_viewer.clear_removable_actors()

        if self.picker_status == PickerStatus.FIND_MPR:
            self.highlight_selected_point(self.point_markers.find_nearest_line(point.image_coordinates[0],
                                                                               get_index=True))

    def add_actor_annotation(self, mouse_x, mouse_y):
        if not self.previous_mouse_coords:
            self.previous_mouse_coords = mouse_x, mouse_y

        if self.picker_status == PickerStatus.PICKING_LENGTH:

            if len(self.length_point_array) == 2:
                print(mouse_x, mouse_y, self.previous_mouse_coords)

                x = self.previous_mouse_coords[0]

                if self.previous_mouse_coords[1] < mouse_y:
                    y = int((mouse_y - self.previous_mouse_coords[1])/2)
                else:
                    y = int((self.previous_mouse_coords[1] - mouse_y)/2)

                vertical_length = round(self.length_point_array.get_vertical_distance()[0], 2)
                total_length = round(self.length_point_array.total_length, 2)
                self.centerline_viewer.add_actor_annotation(x, y,
                                                            f'vert: {vertical_length} mm \n '
                                                            f'total: {total_length} mm')

                self.previous_mouse_coords = None

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
        self.cl_image_properties = CenterlineImageProperties.from_input(input_points=self.point_array,
                                                                        height=self.height,
                                                                        angle=self.angle,
                                                                        input_image=self.original_image_properties)

        self.vtk_data = self.cl_image_properties.vtk_data
        self.nparray = self.cl_image_properties.mpr_np_array
        self.parallel_scale = self.cl_image_properties.get_parallel_scale()

        self.generate_vertical_line_array()

    def generate_vertical_line_array(self):
        vl = VerticalLine(0)
        self.point_markers.add(vl)

        current_location = 0
        for length in self.point_array.lengths:
            current_location += length / self.original_image_properties.spacing[0]
            vl = VerticalLine(current_location)
            self.point_markers.add(vl)

    def highlight_selected_point(self, index):
        if self.has_highlight:
            self.point_markers.show_all()

        self.point_markers.hide_lines_except_index(index)
        self.refresh_panel()

        self.has_highlight = True
        self.case_model.mpr_marker_highlight(index)

    def toggle_mpr_marker(self, show: bool):
        logging.info(f"Toggle MPR marker {show}")
        if show:
            self.point_markers.hide_all()
        else:
            self.point_markers.show_all()
        self.refresh_panel()
