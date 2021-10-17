from MRICenterline.Points.SaveFormatter import SaveFormatter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox

import vtkmodules.all as vtk
from vtkmodules.all import vtkImageData
import qtawesome as qta

from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class CenterlineWidgets:
    def __init__(self, model):
        logging.debug("Initializing Centerline widgets")
        self.model = model

        self.vtk_image_data = vtkImageData()  # initialize blank image data
        self.actor = vtk.vtkImageActor()

    def get_actor(self):
        self.actor.GetMapper().SetInputData(self.model.calculate_input_data())
        self.actor.GetProperty().SetColorLevel(self.model.interface.level)
        self.actor.GetProperty().SetColorWindow(self.model.interface.window)
        return self.actor

    # def save_lengths(self, length_points):
    #     _save_formatter = SaveFormatter(self.model.image_data)
    #     _save_formatter.add_pointcollection_data('length in mpr points', length_points)
    #     _save_formatter.add_generic_data("mpr points", self.model.points)
    #     _save_formatter.save_data()

# ------------------------------ toolbar widgets ------------------------------

    def addSaveAnnotationButton(self):
        _save_button = QPushButton("Save annotations")
        _save_button = QPushButton("Save annotations")
        _save_button.setIcon(qta.icon('fa.save'))
        _save_button.clicked.connect(self.model.save_all)
        return _save_button

    def addLengthPointsButton(self):
        _length_button = QPushButton("Add length points")
        _length_button.setStatusTip("Add length points")
        _length_button.setIcon(qta.icon('fa5s.ruler'))
        _length_button.clicked.connect(self.model.set_points_button_click)
        return _length_button

    def addDisablePointPickingButton(self):
        _disable_picker_button = QPushButton("Disable point picking")
        _disable_picker_button.setStatusTip("Disables active point picker")
        _disable_picker_button.setIcon(qta.icon('fa5.hand-point-up', 'fa5s.ban',
                                                options=[{'scale_factor': 0.5,
                                                          'active': 'fa5.hand-rock'},
                                                         {'color': 'red'}]))
        _disable_picker_button.clicked.connect(self.model.disable_point_picker)
        return _disable_picker_button

    def addUndoButton(self):
        _undo_button = QPushButton("Undo last measurement")
        _undo_button.setStatusTip("Removes last measurement point added")
        _undo_button.setIcon(qta.icon('fa5s.undo-alt'))
        _undo_button.clicked.connect(self.model.undo_annotation)
        return _undo_button

    def addDeleteAllButton(self):
        _delete_all = QPushButton("Clear measurement points")
        _delete_all.setIcon(qta.icon('mdi.delete-outline'))
        _delete_all.clicked.connect(self.model.delete_all_points)
        return _delete_all

    def addTimerButton(self):
        def toggleTimer():
            if not _timer_button.isChecked():
                _timer_button.setIcon(qta.icon('mdi.timer-outline'))
                _timer_button.setText("Start timer")
                self.model.stop_timer()
                _pause_timer_button.setEnabled(False)
            else:
                _timer_button.setIcon(qta.icon('mdi.timer-off-outline'))
                _timer_button.setText("Stop timer")
                self.model.start_timer()
                _pause_timer_button.setEnabled(True)

        def togglePause():
            if not _pause_timer_button.isChecked():
                _pause_timer_button.setIcon(qta.icon("ei.pause-alt"))
                _pause_timer_button.setText("Pause timer")
                self.model.resume_timer()
            else:
                _pause_timer_button.setIcon(qta.icon("ei.play-alt"))
                _pause_timer_button.setText('Resume timer')
                self.model.pause_timer()

        _timer_widget = QWidget()
        _timer_layout = QHBoxLayout()
        _timer_widget.setLayout(_timer_layout)

        _timer_button = QPushButton("Start timer")
        _pause_timer_button = QPushButton("Pause timer")

        _timer_button.setStatusTip("Start timer")
        _timer_button.setIcon(qta.icon('mdi.timer-outline'))
        _timer_button.setCheckable(True)
        _timer_button.clicked.connect(toggleTimer)
        _timer_layout.addWidget(_timer_button)

        _pause_timer_button.setCheckable(True)
        _pause_timer_button.setEnabled(False)
        _pause_timer_button.clicked.connect(togglePause)
        _pause_timer_button.setIcon(qta.icon("ei.pause-alt"))
        _timer_layout.addWidget(_pause_timer_button)

        return _timer_widget

    def addLengthCalculateButton(self):
        _calculate_length = QPushButton("Calculate Length")
        _calculate_length.setIcon(qta.icon('mdi.delete-outline'))
        _calculate_length.clicked.connect(self.model.calculate_length)
        return _calculate_length

    def addHeightSpinbox(self):
        _height_label_widget = QWidget()
        _hbox = QHBoxLayout()
        _height_label_widget.setLayout(_hbox)

        _height_label = QLabel("Height: ")
        self._height_set_box = QDoubleSpinBox()
        self._height_set_box.setMinimumWidth(200)

        self._height_set_box.setMinimum(CONST.CL_MIN_HEIGHT)
        self._height_set_box.setMaximum(CONST.CL_MAX_HEIGHT)
        self._height_set_box.setDecimals(0)
        self._height_set_box.setProperty("value", CONST.CL_INITIAL_HEIGHT)
        self._height_set_box.setSuffix(" mm")

        self._height_set_box.valueChanged.connect(self.model.update_height)

        _hbox.addWidget(_height_label)
        _hbox.addWidget(self._height_set_box)

        return _height_label_widget

    def addAngleSpinbox(self):
        _angle_label_widget = QWidget()
        _hbox = QHBoxLayout()
        _angle_label_widget.setLayout(_hbox)

        _angle_label = QLabel("Angle: ")
        self._angle_set_box = QDoubleSpinBox()
        self._angle_set_box.setMinimumWidth(200)

        self._angle_set_box.setMinimum(CONST.CL_MIN_ANGLE)
        self._angle_set_box.setMaximum(CONST.CL_MAX_ANGLE)
        self._angle_set_box.setDecimals(0)
        self._angle_set_box.setProperty("value", CONST.CL_INITIAL_ANGLE)
        self._angle_set_box.setSuffix(" °")

        self._angle_set_box.valueChanged.connect(self.model.update_angle)

        _hbox.addWidget(_angle_label)
        _hbox.addWidget(self._angle_set_box)

        return _angle_label_widget
