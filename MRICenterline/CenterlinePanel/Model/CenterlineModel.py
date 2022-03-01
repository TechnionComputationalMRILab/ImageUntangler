from MRICenterline.CenterlinePanel.Control.CenterlineWidgets import CenterlineWidgets
from MRICenterline.CenterlinePanel.View.CenterlineViewer import CenterlineViewer
from MRICenterline.CenterlinePanel.Model import Calculate

from MRICenterline.utils.CalculateCenterline import PointsToPlaneVectors
from MRICenterline.Points.SaveFormatter import SaveFormatter

from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class CenterlineModel:
    def __init__(self, image_data, interface):
        self.interface = interface
        self.points = self.interface.points

        self.image_data = image_data
        self.height = CONST.CL_INITIAL_HEIGHT
        self.angle = CONST.CL_INITIAL_ANGLE

        self.control = CenterlineWidgets(model=self)
        self.view = CenterlineViewer(model=self, control=self.control)

    def set_height(self, height):
        self.height = height

    def update_height(self):
        self.view.update_height()

    def update_angle(self):
        self.view.update_angle()

    def set_angle(self, angle):
        self.angle = angle

        # cyclic
        if self.angle == 181:
            self.set_angle(0)
        elif self.angle == -1:
            self.set_angle(180)

    def change_angle(self, angle_change):
        self.set_angle(self.angle + angle_change)

    def get_mpr_properties(self):
        try:
            _mpr_properties = PointsToPlaneVectors(self.points, self.image_data, Plot=0,
                                                   height=self.height, viewAngle=self.angle)
        except Exception as err:
            print(err)
        else:
            return _mpr_properties

    def calculate_input_data(self):
        return Calculate.calculate_input_data(self.get_mpr_properties())

    def set_points_button_click(self):
        logging.debug("Adding length points...")
        self.view.set_points_button_click()

    def save_all(self):
        self.view.save_file()

    def start_timer(self):
        self.view.start_timer()

    def stop_timer(self):
        self.view.stop_timer()

    def pause_timer(self):
        self.view.pause_timer()

    def resume_timer(self):
        self.view.resume_timer()

    def undo_annotation(self):
        self.view.undo_annotation()

    def disable_point_picker(self):
        logging.debug("Disabling point picker")
        self.view.disable_point_picker()

    def delete_all_points(self):
        self.view.delete_all_points()

    def calculate_length(self):
        self.view.calculate_length()
