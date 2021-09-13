from MRICenterline.CenterlinePanel.Control.CenterlineWidgets import CenterlineWidgets
from MRICenterline.CenterlinePanel.View.CenterlineViewer import CenterlineViewer
from MRICenterline.CenterlinePanel.Model import Calculate

from MRICenterline.utils.CalculateCenterline import PointsToPlaneVectors
from MRICenterline.Points.SaveFormatter import SaveFormatter

from MRICenterline.utils import program_constants as CONST
from MRICenterline.Config import ConfigParserRead as CFG

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
        return _mpr_properties

    def calculate_input_data(self):
        return Calculate.calculate_input_data(self.get_mpr_properties())

    def saveLengths(self, filename, length_points):
        self.control.save_lengths(filename, length_points)
        _save_formatter = SaveFormatter(filename, self.image_data)
        _save_formatter.add_pointcollection_data('length in mpr points', length_points)
        _save_formatter.add_generic_data("mpr points", self.points)
        _save_formatter.save_data()
