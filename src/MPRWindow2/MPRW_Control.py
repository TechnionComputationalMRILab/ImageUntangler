import numpy as np
from typing import List
from Model.getMPR import PointsToPlaneVectors
import vtkmodules.all as vtk
from vtk import vtkImageData
from vtk.util import numpy_support
from MPRWindow2.MPRW_ViewerWidget import MPRW_ViewerWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets, mpr_window_config


class MPRW_Control:
    def __init__(self, model):
        self.model = model

        self.vtk_image_data = vtkImageData()  # initialize blank image data
        self.actor = vtk.vtkImageActor()

    def height_angle_groupbox(self) -> QGroupBox:
        _size_set_groupbox = QGroupBox()

        _set_height_angle_layout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        _set_height_angle_layout.addWidget(_height_label)

        self._height_set_box = QDoubleSpinBox(_size_set_groupbox)
        self._height_set_box.valueChanged.connect(self.update_height)
        self._height_set_box.setMinimum(mpr_window_config.height_minmax()[0])
        self._height_set_box.setMaximum(mpr_window_config.height_minmax()[1])
        self._height_set_box.setProperty("value", self.model.height)
        self._height_set_box.setSuffix(" mm")
        _set_height_angle_layout.addWidget(self._height_set_box)

        # angle
        _angle_label = QLabel("Angle")
        _set_height_angle_layout.addWidget(_angle_label)

        self._angle_set_box = QSpinBox(_size_set_groupbox)
        self._angle_set_box.valueChanged.connect(self.update_angle)
        self._angle_set_box.setProperty("value", self.model.angle)
        self._angle_set_box.setSuffix(" °")
        self._angle_set_box.setMaximum(180)
        _set_height_angle_layout.addWidget(self._angle_set_box)

        return _size_set_groupbox

    def update_height(self):
        _height = self._height_set_box.value()
        self.model.set_height(_height)
        print("height")

    def update_angle(self):
        _angle = self._angle_set_box.value()
        self.model.set_angle(_angle)
        print("angle")

    def get_actor(self):
        self.actor.GetMapper().SetInputData(self.model.calculate_input_data())
        return self.actor
