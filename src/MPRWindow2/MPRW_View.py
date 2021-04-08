import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import vtkmodules.all as vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.MPRW_Model import MPRW_Model
from MPRWindow2.MPRInteractor import MPRInteractorStyle
from ast import literal_eval as make_tuple

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRW_View(QWidget):
    def __init__(self, control, parent=None):
        super().__init__(parent=parent)
        self.control = control
        self.model = MPRW_Model(self.control)

        self.MPRW_Top = MPRW_MainQFrame(self.model.calculate_input_data()).frame
        self.MPRW_Bottom = MPRW_Controls()


class MPRW_MainQFrame:
    def __init__(self, input_data):
        self.frame = QFrame()

        self.vl = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setFlat(True)
        self.groupbox.setCheckable(False)
        self.vl.addWidget(self.groupbox)

        self.frame.setLayout(self.vl)

        self.vtkWidget = QVTKRenderWindowInteractor(self.groupbox)
        self.vl.addWidget(self.vtkWidget)

        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.actor = vtk.vtkImageActor()
        self.actor.GetMapper().SetInputData(input_data)
        print(self.actor.GetProperty().GetColorWindow(), self.actor.GetProperty().GetColorLevel())

        self.set_text_actors()
        self.renderer.AddActor(self.actor)

        _bg_colors = self.get_background_from_stylesheet()
        self.renderer.SetBackground(_bg_colors[0]/255, _bg_colors[1]/255, _bg_colors[2]/255)
        self.renderer.ResetCamera()

        self.renderWindow = self.iren.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractorStyle(parent=self.iren, MPRWindow=self)
        self.interactorStyle.SetInteractor(self.iren)
        self.iren.SetInteractorStyle(self.interactorStyle)
        self.renderWindow.SetInteractor(self.iren)

        self.renderWindow.SetInteractor(self.iren)

        self.renderer.GetActiveCamera().ParallelProjectionOn()

        self.renderWindow.Render()

        self.renderer.ResetCamera()
        self.iren.Initialize()

        self.iren.Start()

    def updateWindowAndLevel(self):
        _window = self.actor.GetProperty().GetColorWindow()
        _level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(_window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(_level)))

        # self.textActorAngle.SetInput("Angle: " + str(np.int32(self.MPRViewerProperties.angle)))

    def set_text_actors(self):
        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(1,1,1)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: 525")#?#
        self.renderer.AddActor(self.textActorWindow)

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(1,1,1)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: 1051") #?#)
        self.renderer.AddActor(self.textActorLevel)

        # self.textActorAngle = vtk.vtkTextActor()
        # self.textActorAngle.GetTextProperty().SetFontSize(14)
        # self.textActorAngle.GetTextProperty().SetColor(51/255, 51/255, 1)
        # self.textActorAngle.SetDisplayPosition(0, 47)
        # self.textActorAngle.SetInput("Angle: " + str(angle))
        # self.renderer.AddActor(self.textActorAngle)

    @staticmethod
    def get_background_from_stylesheet():
        _list = [i.split(":") for i in stylesheets.get_sheet_by_name("Default").split(";\n")]
        d = {row[0]:k.strip() for row in _list for k in row[1:]}
        return make_tuple(d["background-color"].strip('rgb'))


class MPRW_Controls(QWidget):
    """ handles the creation of the buttons and boxes"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._bottom_layout = QHBoxLayout()

        self._build_height_angle()
        self._build_length_calc_box()
        self._build_length_results_box()

        self.setLayout(self._bottom_layout)

    def _build_height_angle(self):
        _size_set_groupbox = QGroupBox(self)

        _set_height_angle_layout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        _set_height_angle_layout.addWidget(_height_label)

        _height_set_box = QDoubleSpinBox(_size_set_groupbox)
        _height_set_box.setMaximum(5000.0)
        _height_set_box.setProperty("value", 20.0)
        _height_set_box.setSuffix(" mm")
        _set_height_angle_layout.addWidget(_height_set_box)

        # angle
        _angle_label = QLabel("Angle")
        _set_height_angle_layout.addWidget(_angle_label)
        _angle_set_box = QSpinBox(_size_set_groupbox)
        _angle_set_box.setSuffix(" °")
        _angle_set_box.setMaximum(180)
        _set_height_angle_layout.addWidget(_angle_set_box)

        # update button
        _update_button = QPushButton(_size_set_groupbox)
        _update_button.setText("Update")
        _set_height_angle_layout.addWidget(_update_button)

        self._bottom_layout.addWidget(_size_set_groupbox)

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
