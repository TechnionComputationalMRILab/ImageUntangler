import vtk
from MPRwindow import MPRInteractor
import numpy as np
from vtk import vtkImageData
from vtk.util import numpy_support
from Model import getMPR
from MPRwindow.MPRViewerProperties import viewerLogic
from Model.PointCollection import PointCollection
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class View:
    def __init__(self, interactor: QVTKRenderWindowInteractor, MPRViewerProperties: viewerLogic):
        self.interactor = interactor
        self.MPRViewerProperties = MPRViewerProperties
        self.lengthPoints = PointCollection()
        self.Visualize_MPR()

    def Visualize_MPR(self):
        MPR_M = self.MPRViewerProperties.MPR_M
        delta = self.MPRViewerProperties.delta
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
        scalars = numpy_support.numpy_to_vtk(num_array=MPR_M.ravel(), deep=True, array_type=vtk_datatype)

        MPR_vtk.GetPointData().SetScalars(scalars)
        MPR_vtk.Modified()
        self.actor = vtk.vtkImageActor()
        self.actor.GetMapper().SetInputData(MPR_vtk)


        #Renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(171/255,216/255,1)
        self.renderer.ResetCamera()

        # self.interactor = QVTKRenderWindowInteractor(self.groupBox)
        # self.gridLayout.addWidget(self.interactor, 0, 0, 1, 3)
        self.renderWindow = self.interactor.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractor.MPRInteractorStyle(parent=self.interactor, MPRWindow=self)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.renderWindow.SetInteractor(self.interactor)


        #renderWindowInteractor = vtk.vtkRenderWindowInteractor()

        self.renderWindow.SetInteractor(self.interactor)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()
        self.interactor.Initialize()
        #interactor.Start()

        # self.MPRViewerProperties.window = self.actor.GetProperty().GetColorWindow()
        # self.MPRViewerProperties.level = self.actor.GetProperty().GetColorLevel()

        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: 525")#?#
        self.renderer.AddActor(self.textActorWindow)

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: 1051") #?#)
        self.renderer.AddActor(self.textActorLevel)

        self.textActorAngle = vtk.vtkTextActor()
        self.textActorAngle.GetTextProperty().SetFontSize(14)
        self.textActorAngle.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorAngle.SetDisplayPosition(0, 47)
        self.textActorAngle.SetInput("Angle: " + str(self.MPRViewerProperties.angle))
        self.renderer.AddActor(self.textActorAngle)


        self.renderWindow.Render()
        # self.interactor.Start()

    def updateWindowAndLevel(self):
        self.MPRViewerProperties.window = self.actor.GetProperty().GetColorWindow()
        self.MPRViewerProperties.level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.MPRViewerProperties.window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.MPRViewerProperties.level)))
        self.textActorAngle.SetInput("Angle: " + str(np.int32(self.MPRViewerProperties.angle)))
        self.renderWindow.Render()

    def changeAngle(self, angle):
        Height = self.MPRViewerProperties.Height
        self.MPRViewerProperties.angle = angle
        GetMPR = getMPR.PointsToPlaneVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.originalPoints,
                                             self.MPRViewerProperties.ConvViewMode, height=Height, viewAngle=angle, Plot=0)
        self.MPRViewerProperties.MPR_M = GetMPR.MPR_M
        self.MPRViewerProperties.delta = GetMPR.delta
        self.MPRViewerProperties.MPRposition = GetMPR.MPR_indexs_np

        # MPRWindow.Ui_MPRWindow.spinBox.setValue(angle)

        self.Visualize_MPR()
        self.updateWindowAndLevel()

    def processNewPoint(self, pickedCoordinates):
        coordinates = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], 0] # x,y,z,sliceIdx
        if self.lengthPoints.addPoint(coordinates): # if did not already exist
            currentPolygonActor = self.lengthPoints.generatePolygonLastPoint(pickedCoordinates) # generate polygon for the point we just added
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints()

    def presentPoints(self):
        for point in self.lengthPoints.points:
            polygon = point.polygon
            polygon.GeneratePolygonOn()
            self.renderWindow.Render()