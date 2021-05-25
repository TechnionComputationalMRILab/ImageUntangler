import numpy as np
from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D
import vtkmodules.all as vtk

from Model import ImageProperties
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from Model.PointCollection import PointCollection
from MPRWindow.MPRWindow import MPRWindow
from MainWindowComponents import MessageBoxes
from Control.SaveFormatter import SaveFormatter
from Control.PointLoader import PointLoader
from icecream import ic

from util import logger
logger = logger.get_logger()


class BaseSequenceViewer:
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor, interactorStyle: SequenceViewerInteractorStyle, imagePath: str, isDicom = False):
        self.manager = manager
        self.interactor = interactor
        self.imageData = ImageProperties.getImageData(imagePath, isDicom)
        self.LevelVal = (self.imageData.dicomArray.max()+self.imageData.dicomArray.min())/2
        self.WindowVal = self.imageData.dicomArray.max()-self.imageData.dicomArray.min()
        self.actor = vtkImageActor()
        self.renderer = vtkRenderer()
        # self.window: QVTKRenderWindowInteractor = interactor
        self.window = self.interactor.GetRenderWindow()
        self.interactorStyle = interactorStyle
        self.reslice = vtkImageReslice()

        self.Cursor = vtkCursor2D()
        self.performReslice()
        self.connectActor()
        self.renderImage()

        self.MPRpoints = PointCollection()
        self.lengthPoints = PointCollection()
        self.index_list = []

        self.presentCursor()

    def performReslice(self):
        # Extract a slice in the desired orientation
        x0, y0, z0 = self.imageData.origin
        x_spacing, y_spacing, z_spacing = self.imageData.spacing
        x_min, x_max, y_min, y_max, z_min, z_max = self.imageData.extent

        center = [x0 + x_spacing * 0.5 * (x_min + x_max),
                       y0 + y_spacing * 0.5 * (y_min + y_max),
                       z0 + z_spacing * 0.5 * (z_min + z_max)]
        transformation = vtkMatrix4x4()
        transformation.DeepCopy((1, 0, 0, center[0],
                             0, -1, 0, center[1],
                             0, 0, 1, center[2],
                             0, 0, 0, 1))
        self.reslice.SetInputData(self.imageData.fullData)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

    def connectActor(self):
        self.actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.actor.GetProperty().SetColorWindow(self.WindowVal)
        self.actor.GetProperty().SetColorLevel(self.LevelVal)

    def renderImage(self):
        logger.info(f"Rendering Image {self.imageData.header['filename']}")
        self.renderer.SetBackground(204 / 255, 204 / 255, 204 / 255)
        self.renderer.AddActor(self.actor)
        self.renderer.SetLayer(0)
        # self.window = self.interactor.GetRenderWindow()
        self.window.AddRenderer(self.renderer)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.window.SetInteractor(self.interactor)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().SetParallelScale(self.imageData.getParallelScale())

    def setIdxText(self):
        self.textActorSliceIdx = vtkTextActor()
        self.textActorSliceIdx.GetTextProperty().SetFontSize(14)
        self.textActorSliceIdx.GetTextProperty().SetColor(0, 34/255, 158/255)
        self.textActorSliceIdx.SetDisplayPosition(0, 2)
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(self.sliceIdx))
        self.renderer.AddActor(self.textActorSliceIdx)

    def setWindowText(self):
        self.textActorWindow = vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(0, 34/255, 158/255)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: " + str(self.WindowVal))
        self.renderer.AddActor(self.textActorWindow)

    def setLevelText(self):
        self.textActorLevel = vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(0, 34/255, 158/255)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: " + str(self.LevelVal))
        self.renderer.AddActor(self.textActorLevel)

    def adjustWindow(self, window: int):
        self.actor.GetProperty().SetColorWindow(window)
        self.WindowVal = window
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.WindowVal)))
        self.window.Render()

    def adjustLevel(self, level: int):
        self.actor.GetProperty().SetColorLevel(level)
        self.LevelVal = level
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.LevelVal)))
        self.window.Render()

    def updateWindowLevel(self):
        logger.debug(f"Window and Level updated to ({self.actor.GetProperty().GetColorWindow()}, {self.actor.GetProperty().GetColorLevel()})")
        self.manager.changeWindow(self.actor.GetProperty().GetColorWindow())
        self.manager.changeLevel(self.actor.GetProperty().GetColorLevel())

    def processNewPoint(self, pointCollection, pickedCoordinates, color=(1, 0, 0)):
        raise NotImplementedError

    # def addPoint(self, pointType, pickedCoordinates):
    #     raise NotImplementedError

    def presentCursor(self):
        self.Cursor.SetModelBounds(-10000, 10000, -10000, 10000, 0, 0)
        self.Cursor.SetFocalPoint(0, 0, 0)
        self.Cursor.AxesOn()
        self.Cursor.TranslationModeOn()
        self.Cursor.OutlineOff()
        cursorMapperAx = vtkPolyDataMapper()
        cursorMapperAx.SetInputConnection(self.Cursor.GetOutputPort())
        cursorActorAx = vtkActor()
        cursorActorAx.SetMapper(cursorMapperAx)
        cursorActorAx.GetProperty().SetColor(1, 0, 0)
        self.renderer.AddActor(cursorActorAx)

    def Start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    def updateZoomFactor(self):
        curParallelScale = self.renderer.GetActiveCamera().GetParallelScale()
        newZoomFactor = curParallelScale / self.imageData.getParallelScale()
        self.renderer.GetActiveCamera().SetParallelScale(self.imageData.getParallelScale() * newZoomFactor)
        self.window.Render()

    def UpdateViewerMatrixCenter(self, center: List[int], sliceIdx):
        matrix = self.reslice.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(sliceIdx))
        self.window.Render()
        self.sliceIdx = sliceIdx
        self.imageData.sliceIdx = sliceIdx
        self.manager.updateSliderIndex(self.sliceIdx)
        self.presentPoints(self.MPRpoints, sliceIdx)

    def presentPoints(self, pointCollection, sliceIdx) -> None:
        raise NotImplementedError

    def moveBullsEye(self, newCoordinates):
        self.Cursor.SetFocalPoint(newCoordinates)
        self.window.Render()

    def addPoint(self, pointType, pickedCoordinates):
        if pointType.upper() == "MPR":
            self.processNewPoint(self.MPRpoints, pickedCoordinates, color=(1, 0, 0))
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, pickedCoordinates, color=(55/255, 230/255, 128/255))

    def calculateLengths(self):
        if len(self.lengthPoints) >= 2:
            pointsPositions = np.asarray(self.lengthPoints.getCoordinatesArray())
            allLengths = [np.linalg.norm(pointsPositions[j, :] - pointsPositions[j + 1, :]) for j in
                          range(len(pointsPositions) - 1)]
            totalDistance = np.sum(allLengths)
            print(totalDistance)
            print(allLengths)
        else:
            MessageBoxes.notEnoughPointsClicked("length")

    def calculateMPR(self):
        if self.MPRpoints.getCoordinatesArray().shape[0] <= 3:
            MessageBoxes.notEnoughPointsClicked("MPR")
        else:
            MPRWindow(self.MPRpoints.getCoordinatesArray(), self.imageData)

    def saveLengths(self, filename):
        _save_formatter = SaveFormatter(filename, self.imageData)
        _save_formatter.add_pointcollection_data('length points', self.lengthPoints)
        _save_formatter.save_data()

    def saveMPRPoints(self, filename):
        _save_formatter = SaveFormatter(filename, self.imageData)
        _save_formatter.add_pointcollection_data("MPR points", self.MPRpoints)
        _save_formatter.save_data()

    def loadMPRPoints(self, filename):
        logger.info(f"Loading MPR points from {filename}")
        _mpr_loader = PointLoader(filename, self.imageData)
        self.MPRpoints = _mpr_loader.get_points()

    def drawLengthLines(self):
        if len(self.lengthPoints) >= 2:
            _actor = self.lengthPoints.generateLineActor()

            _renderer = vtkRenderer()
            _renderer.AddActor(_actor)
            print(_actor.GetBounds())

            _renderer.InteractiveOn() # TODO: fix me

            self.window.AddRenderer(_renderer)
            _renderer.SetLayer(1)
            self.window.SetNumberOfLayers(2)

            self.window.Render()

    def drawMPRSpline(self):
        if self.MPRpoints.getCoordinatesArray().shape[0] >= 3:
            _actor = self.MPRpoints.generateSplineActor()

            _renderer = vtkRenderer()
            _renderer.AddActor(_actor)
            _renderer.InteractiveOn() # TODO: IS TEMPORARY

            self.window.AddRenderer(_renderer)
            _renderer.SetLayer(1)
            self.window.SetNumberOfLayers(2)

            self.window.Render()
