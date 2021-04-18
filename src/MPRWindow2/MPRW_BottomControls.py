import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from icecream import ic

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets, mpr_window_config


class MPRW_BottomControls(QWidget):
    """ handles the creation of the buttons and boxes"""
    def __init__(self, model, control, parent=None):
        super(MPRW_BottomControls, self).__init__(parent=parent)
        self.model = model
        self.control = control

        _bottom_layout = QHBoxLayout()
        _bottom_layout.addWidget(self.control.height_angle_groupbox())
        # self._build_height_angle()
        # self._build_length_calc_box()
        # self._build_length_results_box()

        self.setLayout(_bottom_layout)

    def _build_height_angle(self):
        _size_set_groupbox = QGroupBox(self)

        _set_height_angle_layout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        _set_height_angle_layout.addWidget(_height_label)

        self._height_set_box = QDoubleSpinBox(_size_set_groupbox)
        self._height_set_box.valueChanged.connect(self._update_height)
        self._height_set_box.setMinimum(mpr_window_config.height_minmax()[0])
        self._height_set_box.setMaximum(mpr_window_config.height_minmax()[1])
        self._height_set_box.setProperty("value", self.model.height)
        self._height_set_box.setSuffix(" mm")
        _set_height_angle_layout.addWidget(self._height_set_box)

        # angle
        _angle_label = QLabel("Angle")
        _set_height_angle_layout.addWidget(_angle_label)

        self._angle_set_box = QSpinBox(_size_set_groupbox)
        self._angle_set_box.valueChanged.connect(self._update_angle)
        self._angle_set_box.setProperty("value", self.model.angle)
        self._angle_set_box.setSuffix(" °")
        self._angle_set_box.setMaximum(180)
        _set_height_angle_layout.addWidget(self._angle_set_box)

        self._bottom_layout.addWidget(_size_set_groupbox)

    # def _update_height(self):
    #
    #     print(_height)
    #
    # def _update_angle(self):
    #     # _angle = self._angle_set_box.value()
    #     print("angle changed")

    def _build_length_calc_box(self):
        _length_calc_groupbox = QGroupBox(self)

        _length_calc_layout = QVBoxLayout(_length_calc_groupbox)

        _set_points_button = QPushButton("Set Points")
        _length_calc_layout.addWidget(_set_points_button)

        _calc_length_button = QPushButton("Calculate Length")
        _length_calc_layout.addWidget(_calc_length_button)

        _save_button = QPushButton("Save")
        _length_calc_layout.addWidget(_save_button)

        self._bottom_layout.addWidget(_length_calc_groupbox)

    def _build_length_results_box(self):
        _length_results_group_box = QGroupBox(self)

        _length_results_layout = QVBoxLayout(_length_results_group_box)

        _length_results_label = QLabel("Calculated Length")

        _font = QFont()
        _font.setBold(True)
        _font.setWeight(75)
        _length_results_label.setFont(_font)

        _length_results_layout.addWidget(_length_results_label)

        self._bottom_layout.addWidget(_length_results_group_box)
