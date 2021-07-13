import numpy as np
from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D
import vtkmodules.all as vtk

from MRICenterline.DisplayPanel.Model import ImageProperties
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MRICenterline.Points.PointCollection import PointCollection
from MRICenterline.Points.LoadPoints import LoadPoints
from MRICenterline.Points.SaveFormatter import SaveFormatter

# from icecream import ic

from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class GenericSequenceViewer:
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor, interactorStyle: SequenceViewerInteractorStyle, image):
        self.manager = manager
        self.interactor = interactor

        self.actor = vtkImageActor()
        self.renderer = vtkRenderer()

        # self.imageData = ImageProperties.getImageData(imager, sequence="")
        self.imageData = image
        self.LevelVal = (self.imageData.dicomArray.max()+self.imageData.dicomArray.min())/2
        self.WindowVal = self.imageData.dicomArray.max()-self.imageData.dicomArray.min()

        self.sliceIdx = self.imageData.sliceIdx
        self.pastIndex = self.sliceIdx
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()

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

        self.presentCursor()

        logging.debug("Rendering sequence")
        self.window.Render()

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
        self.reslice.SetInputData(self.imageData.full_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

    def connectActor(self):
        self.actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.actor.GetProperty().SetColorWindow(self.WindowVal)
        self.actor.GetProperty().SetColorLevel(self.LevelVal)

    def renderImage(self):
        logging.info(f"Rendering Image {self.imageData.header['filename'][0]}, etc...")
        self.renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
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
        logging.debug(f"Window and Level updated to ({self.actor.GetProperty().GetColorWindow()}, {self.actor.GetProperty().GetColorLevel()})")
        self.manager.changeWindow(self.actor.GetProperty().GetColorWindow())
        self.manager.changeLevel(self.actor.GetProperty().GetColorLevel())

    def processNewPoint(self, pointCollection, pickedCoordinates, color=(1, 0, 0)):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], self.sliceIdx]  # x,y,z,sliceIdx

        if pointCollection.addPoint(pointLocation):
            currentPolygonActor = pointCollection.generatePolygonLastPoint(color)
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(pointCollection, self.sliceIdx)

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

    def moveBullsEye(self, newCoordinates):
        self.Cursor.SetFocalPoint(newCoordinates)
        self.window.Render()

    def addPoint(self, pointType, pickedCoordinates):
        if pointType.upper() == "MPR":
            self.processNewPoint(self.MPRpoints, pickedCoordinates, color=CFG.get_color('mpr-display-style'))
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, pickedCoordinates, color=CFG.get_color('length-display-style'))

    def calculateLengths(self):
        if len(self.lengthPoints) >= 2:
            pointsPositions = np.asarray(self.lengthPoints.getCoordinatesArray())
            allLengths = [np.linalg.norm(pointsPositions[j, :] - pointsPositions[j + 1, :]) for j in
                          range(len(pointsPositions) - 1)]
            totalDistance = np.sum(allLengths)
            print(totalDistance)
            print(allLengths)
        else:
            pass
            # MessageBoxes.notEnoughPointsClicked("length")

    def calculateMPR(self):
        self.manager.showCenterlinePanel()
        # if self.MPRpoints.getCoordinatesArray().shape[0] <= 3:
        #     pass
        #     # MessageBoxes.notEnoughPointsClicked("MPR")
        # else:
        #     self.manager.addWidget(CenterlinePanel)
        #     # TODO: MPRPanel
        #     # MPRWindow(self.MPRpoints.getCoordinatesArray(), self.imageData)

    def saveLengths(self, filename):
        _save_formatter = SaveFormatter(filename, self.imageData)
        _save_formatter.add_pointcollection_data('length points', self.lengthPoints)
        _save_formatter.save_data()

    def saveMPRPoints(self, filename):
        _save_formatter = SaveFormatter(filename, self.imageData)
        _save_formatter.add_pointcollection_data("MPR points", self.MPRpoints)
        _save_formatter.save_data()

    def loadLengthPoints(self, filename):
        logging.info(f"Loading length points from {filename}")
        _length_loader = LoadPoints(filename, self.imageData)

        for point in _length_loader.get_points():
            self.lengthPoints.addPoint(point.coordinates)
            currentPolygonActor = self.lengthPoints.generatePolygonLastPoint(color=CFG.get_color('length-display-style'))
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(self.lengthPoints, self.sliceIdx)

    def loadMPRPoints(self, filename):
        logging.info(f"Loading MPR points from {filename}")
        _mpr_loader = LoadPoints(filename, self.imageData)

        for point in _mpr_loader.get_points():
            self.MPRpoints.addPoint(point.coordinates)
            currentPolygonActor = self.MPRpoints.generatePolygonLastPoint(color=CFG.get_color('mpr-display-style'))
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(self.MPRpoints, self.sliceIdx)

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

    def showMPRPanel(self):
        print("show mpr panel placeholder")

    def modifyAnnotation(self, x, y):
        logging.debug("modifyAnnotation function activated")

        _prop_picker = vtk.vtkPicker()
        _prop_picker.SetTolerance(50)

        _found_props = []

        if _prop_picker.Pick(x, y, 0, self.renderer):
            logging.info(f"Prop picked at {x}, {y}.")
            # ic(_prop_picker.GetProp3Ds().GetLastProp3D())
            # _found_props.append(_prop_picker.GetViewProp())
        # else:
        #     _found_props = list(set(_found_props))
        #     if _found_props:
        #         for i in _found_props:
        #             if not isinstance(i, vtkImageActor):
            return _prop_picker.GetProp3Ds().GetLastProp3D()
        else:
            logging.info(f"No prop found at {x}, {y}.")

    def deleteAnnotation(self, x, y, prop):
        logging.debug("deleteAnnotation function activated")

        print(f'Deleting {prop} at {x}, {y}.')
        self.renderer.RemoveActor(prop)

    def presentPoints(self, pointCollection, sliceIdx) -> None:
        logging.debug(f"{len(pointCollection)} points in memory")
        for point in pointCollection.points:
            polygon = point.polygon
            # ic(polygon)
            if point.coordinates[3] != sliceIdx:  # dots were placed on different slices
                polygon.GeneratePolygonOff()
            else:
                polygon.GeneratePolygonOn()
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

    def setSliceIndex(self, index: int):
        self.reslice.Update()
        sliceSpacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, (index-self.pastIndex)*sliceSpacing, 1))
        if 0 <= index <= self.imageData.extent[5]:
            self.pastIndex = index
            self.UpdateViewerMatrixCenter(center, index)
        else:
            print("INVALID INDEX ISSUE: PLEASE NOTIFY DEVELOPERS")

    def adjustSliceIdx(self, changeFactor: int):
        # changeFactor determines by how much to change the index
        self.reslice.Update()
        sliceSpacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, changeFactor*sliceSpacing, 1))
        sliceIdx = int((center[2] - self.imageData.origin[2]) /
                       self.imageData.spacing[2] - 0.5)  # z - z_orig/(z_spacing - .5). slice idx is z coordinate of slice of image
        if 0 <= sliceIdx <= self.imageData.extent[5]:
            self.pastIndex = sliceIdx
            self.UpdateViewerMatrixCenter(center, sliceIdx)

