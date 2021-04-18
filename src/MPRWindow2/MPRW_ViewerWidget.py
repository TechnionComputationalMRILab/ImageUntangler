import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import vtkmodules.all as vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.MPRInteractor import MPRInteractorStyle
from ast import literal_eval as make_tuple
from icecream import ic

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets, mpr_window_config


class MPRW_ViewerWidget(QFrame):
    def __init__(self, model, control, parent=None):
        super(MPRW_ViewerWidget, self).__init__(parent=parent)
        self.model = model
        self.control = control

        self.vl = QVBoxLayout()
        # self.groupbox = QGroupBox()
        # self.groupbox.setFlat(True)
        # self.groupbox.setCheckable(False)
        # self.vl.addWidget(self.groupbox)

        self.setLayout(self.vl)

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vl.addWidget(self.vtkWidget)

        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # self.actor = vtk.vtkImageActor()
        # self.actor.GetMapper().SetInputData(self.model.calculate_input_data())

        self.set_text_actors()
        # self.renderer.AddActor(self.actor)
        self.renderer.AddActor(self.control.get_actor())

        _bg_colors = self.get_background_from_stylesheet()
        self.renderer.SetBackground(_bg_colors[0]/255, _bg_colors[1]/255, _bg_colors[2]/255)
        self.renderer.ResetCamera()

        self.renderWindow = self.iren.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractorStyle(parent=self.iren, MPRWindow=self)
        self.interactorStyle.SetInteractor(self.iren)
        self.iren.SetInteractorStyle(self.interactorStyle)
        self.renderWindow.SetInteractor(self.iren)

        self.renderWindow.Render()
        self.renderer.ResetCamera()
        self.iren.Initialize()
        self.iren.Start()

    def update_height(self):
        self.actor.GetMapper().SetInputData(self.model.calculate_input_data())
        self.renderWindow.Render()

    def update_angle(self):
        self.iren.ReInitialize()

    def updateWindowAndLevel(self):
        _window = self.actor.GetProperty().GetColorWindow()
        _level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(_window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(_level)))
        # self.textActorAngle.SetInput("Angle: " + str(np.int32(self.input.viewAngle)))

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
        # self.textActorAngle.SetInput("Angle: " + str(self.input.viewAngle))
        # self.renderer.AddActor(self.textActorAngle)

    @staticmethod
    def get_background_from_stylesheet():
        _list = [i.split(":") for i in stylesheets.get_sheet_by_name("Default").split(";\n")]
        d = {row[0]:k.strip() for row in _list for k in row[1:]}
        return make_tuple(d["background-color"].strip('rgb'))
