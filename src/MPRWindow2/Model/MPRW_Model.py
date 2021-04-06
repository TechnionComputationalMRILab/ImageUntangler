import vtk
import numpy as np
from vtk import vtkImageData
from vtk.util import numpy_support as npvtk
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from Model import getMPR
from MPRwindow.MPRViewerProperties import viewerLogic
from Model.PointCollection import PointCollection
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.Control.MPRW_Control import MPRW_Control
from MPRWindow2.Control.MPRInteractor import MPRInteractorStyle
from icecream import ic

import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRW_Model:
    def __init__(self, input_data: MPRW_Control):
        self.frame = QFrame()

        self.vl = QVBoxLayout()
        self.interactor = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.interactor)
        self.frame.setLayout(self.vl)

        self.control = input_data
        self.control.set_angle(0)
        self.control.set_height(20)

        self.lengthPoints = PointCollection()

        self.Visualize_MPR()

    def Visualize_MPR(self):
        MPR_M = self.control.MPR_M
        delta = self.control.delta
        n = MPR_M.shape[0]
        m = MPR_M.shape[1]
        MPR_vtk = vtkImageData()
        MPR_vtk.SetDimensions(n, m, 1)
        MPR_vtk.SetOrigin([0, 0, 0])
        MPR_vtk.SetSpacing([delta, delta, delta])

        vtk_type_by_numpy_type = {
            np.uint8: vtk.VTK_UNSIGNED_CHAR,
            np.uint16: vtk.VTK_UNSIGNED_SHORT,
            np.uint32: vtk.VTK_UNSIGNED_INT,
            np.uint64: vtk.VTK_UNSIGNED_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_UNSIGNED_LONG_LONG,
            np.int8: vtk.VTK_CHAR,
            np.int16: vtk.VTK_SHORT,
            np.int32: vtk.VTK_INT,
            np.int64: vtk.VTK_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_LONG_LONG,
            np.float32: vtk.VTK_FLOAT,
            np.float64: vtk.VTK_DOUBLE
        }

        vtk_datatype = vtk_type_by_numpy_type[MPR_M.dtype.type]
        MPR_M = np.transpose(MPR_M)
        scalars = npvtk.numpy_to_vtk(num_array=MPR_M.ravel(), deep=True, array_type=vtk_datatype)

        MPR_vtk.GetPointData().SetScalars(scalars)
        MPR_vtk.Modified()
        self.actor = vtk.vtkImageActor()
        self.actor.GetMapper().SetInputData(MPR_vtk)

        #Renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractorStyle(parent=self.interactor, MPRWindow=self)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)

        self.renderer.SetBackground(68/255, 71/255, 79/255) # TODO: get this from defaultbackground.css instead
        self.renderer.ResetCamera()

        self.renderWindow.AddRenderer(self.renderer)
        self.renderWindow.SetInteractor(self.interactor)

        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()

        self.control.window = self.actor.GetProperty().GetColorWindow()
        self.control.level = self.actor.GetProperty().GetColorLevel()

        self.set_text_actors()
        self.renderWindow.Render()
        self.interactor.Initialize()
        # self.interactor.Start()

    def set_text_actors(self):
        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(1, 1, 1)  # TODO: set this from elsewhere
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: 525")#?#
        self.renderer.AddActor(self.textActorWindow)

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(1, 1, 1)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: 1051") #?#)
        self.renderer.AddActor(self.textActorLevel)

        self.textActorAngle = vtk.vtkTextActor()
        self.textActorAngle.GetTextProperty().SetFontSize(14)
        self.textActorAngle.GetTextProperty().SetColor(1, 1, 1)
        self.textActorAngle.SetDisplayPosition(0, 47)
        self.textActorAngle.SetInput("Angle: " + str(self.control.angle))
        self.renderer.AddActor(self.textActorAngle)

    def update_window_and_level(self):
        self.control.window = self.actor.GetProperty().GetColorWindow()
        self.control.level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.control.window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.control.level)))
        self.textActorAngle.SetInput("Angle: " + str(np.int32(self.control.angle)))
        self.renderWindow.Render()

    def change_angle(self, angle):
        pass

    def change_height(self, height):
        pass

    def process_new_point(self, coords):
        coordinates = [coords[0], coords[1], coords[2], 0] # x,y,z,sliceIdx
        if self.lengthPoints.addPoint(coordinates): # if did not already exist
            currentPolygonActor = self.lengthPoints.generatePolygonLastPoint(coords) # generate polygon for the point we just added
            self.renderer.AddActor(currentPolygonActor)
        self.present_points()

    def present_points(self):
        for point in self.lengthPoints.points:
            polygon = point.polygon
            polygon.GeneratePolygonOn()
            self.renderWindow.Render()


