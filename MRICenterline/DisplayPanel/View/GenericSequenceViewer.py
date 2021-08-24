import numpy as np
from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D
import vtkmodules.all as vtk

from MRICenterline.Points.PointArray import PointArray
from MRICenterline.DisplayPanel.Model import ImageProperties
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MRICenterline.Points.PointCollection import PointCollection
from MRICenterline.Points.LoadPoints import LoadPoints
from MRICenterline.Points.SaveFormatter import SaveFormatter

from MRICenterline.utils import message as MSG
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class GenericSequenceViewer:
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor, interactorStyle: SequenceViewerInteractorStyle, image):
        self.manager = manager
        self.interactor = interactor

        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()

        # self.imageData = ImageProperties.getImageData(imager, sequence="")
        self.imageData = image

        # self.LevelVal = (self.imageData.dicomArray.max()+self.imageData.dicomArray.min())/2
        # self.WindowVal = self.imageData.dicomArray.max()-self.imageData.dicomArray.min()

        self.LevelVal = self.imageData.level_value
        self.WindowVal = self.imageData.window_value

        self.sliceIdx = self.imageData.sliceIdx
        self.pastIndex = self.sliceIdx
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()

        # self.window: QVTKRenderWindowInteractor = interactor
        self.window = self.interactor.GetRenderWindow()
        self.interactorStyle = interactorStyle
        self.reslice = vtkImageReslice()

        # self.window.AddRenderer(self.annotation_renderer)
        # self.annotation_renderer.SetLayer(1)
        # self.window.SetNumberOfLayers(2)

        self.Cursor = vtkCursor2D()
        self.performReslice()
        self.connectActor()
        self.renderImage()

        # self.MPRpoints = PointCollection()
        self.MPRpoints = PointArray()
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
        self.panel_actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.panel_actor.GetProperty().SetColorWindow(self.WindowVal)
        self.panel_actor.GetProperty().SetColorLevel(self.LevelVal)

    def renderImage(self):
        logging.info(f"Rendering Image {self.imageData.header['filename'][0]}, etc...")
        self.panel_renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.panel_renderer.AddActor(self.panel_actor)
        self.panel_renderer.SetLayer(0)
        # self.window = self.interactor.GetRenderWindow()
        self.window.AddRenderer(self.panel_renderer)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.window.SetInteractor(self.interactor)
        self.panel_renderer.GetActiveCamera().ParallelProjectionOn()
        self.panel_renderer.ResetCamera()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.imageData.getParallelScale())

    def setIdxText(self):
        _display_color = CFG.get_color('display')
        _order = CONST.ORDER_OF_CONTROLS.index('Slice Index')

        self.textActorSliceIdx = vtkTextActor()
        self.textActorSliceIdx.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.textActorSliceIdx.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorSliceIdx.SetDisplayPosition(0, _order*int(CFG.get_config_data('display', 'font-size')))
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(self.sliceIdx))
        self.panel_renderer.AddActor(self.textActorSliceIdx)

    def setWindowText(self):
        _display_color = CFG.get_color('display')
        _order = CONST.ORDER_OF_CONTROLS.index('Window')

        self.textActorWindow = vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.textActorWindow.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorWindow.SetDisplayPosition(0, _order*int(CFG.get_config_data('display', 'font-size')))
        self.textActorWindow.SetInput("Window: " + str(self.WindowVal))
        self.panel_renderer.AddActor(self.textActorWindow)

    def setLevelText(self):
        _display_color = CFG.get_color('display')
        _order = CONST.ORDER_OF_CONTROLS.index('Level')

        self.textActorLevel = vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.textActorLevel.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorLevel.SetDisplayPosition(0, _order*int(CFG.get_config_data('display', 'font-size')))
        self.textActorLevel.SetInput("Level: " + str(self.LevelVal))
        self.panel_renderer.AddActor(self.textActorLevel)

    def adjustWindow(self, window: int):
        self.panel_actor.GetProperty().SetColorWindow(window)
        self.WindowVal = window
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.WindowVal)))
        self.window.Render()

    def adjustLevel(self, level: int):
        self.panel_actor.GetProperty().SetColorLevel(level)
        self.LevelVal = level
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.LevelVal)))
        self.window.Render()

    def updateWindowLevel(self):
        logging.debug(f"Window and Level updated to ({self.panel_actor.GetProperty().GetColorWindow()}, {self.panel_actor.GetProperty().GetColorLevel()})")
        self.manager.changeWindow(self.panel_actor.GetProperty().GetColorWindow())
        self.manager.changeLevel(self.panel_actor.GetProperty().GetColorLevel())

    def processNewPoint(self, pointCollection, pickedCoordinates, color=(1, 0, 0), size=1):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], self.sliceIdx]  # x,y,z,sliceIdx

        if pointCollection.addPoint(pointLocation):
            currentPolygonActor = pointCollection.generatePolygonLastPoint(color, size)
            self.panel_renderer.AddActor(currentPolygonActor)

        # self.presentPoints(pointCollection, self.sliceIdx)
        self.render_panel()

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
        self.panel_renderer.AddActor(cursorActorAx)

    def Start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    def updateZoomFactor(self):
        curParallelScale = self.panel_renderer.GetActiveCamera().GetParallelScale()
        newZoomFactor = curParallelScale / self.imageData.getParallelScale()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.imageData.getParallelScale() * newZoomFactor)
        self.window.Render()

    def moveBullsEye(self, newCoordinates):
        self.Cursor.SetFocalPoint(newCoordinates)
        self.window.Render()

    def addPoint(self, pointType, pickedCoordinates):
        if pointType.upper() == "MPR":
            self.processNewPoint(self.MPRpoints, pickedCoordinates,
                                 color=CFG.get_color('mpr-display-style'),
                                 size=int(CFG.get_config_data('mpr-display-style', 'marker-size')))
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, pickedCoordinates,
                                 color=CFG.get_color('length-display-style'),
                                 size=int(CFG.get_config_data('length-display-style', 'marker-size')))

    def calculateLengths(self):
        if len(self.lengthPoints) >= 2:
            # ic(self.lengthPoints.getCoordinatesArray())
            pointsPositions = np.asarray(self.lengthPoints.getCoordinatesArray())
            allLengths = [np.linalg.norm(pointsPositions[j, :] - pointsPositions[j + 1, :]) for j in
                          range(len(pointsPositions) - 1)]
            totalDistance = np.sum(allLengths)

            strdis = ["{0:.2f}".format(allLengths[i]) for i in range(len(allLengths))]

            MSG.msg_box_info("Calculated length",
                             info="The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),"{0:.2f}".format(totalDistance)))

        else:
            MSG.msg_box_warning("Not enough points clicked to calculate length")

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
            self.lengthPoints.addPoint(point.image_coordinates)
            currentPolygonActor = self.lengthPoints.generatePolygonLastPoint(color=CFG.get_color('length-display-style'))
            self.panel_renderer.AddActor(currentPolygonActor)
        # self.presentPoints(self.lengthPoints, self.sliceIdx)

    def loadMPRPoints(self, filename):
        logging.info(f"Loading MPR points from {filename}")
        _mpr_loader = LoadPoints(filename, self.imageData)

        for point in _mpr_loader.get_points():
            self.MPRpoints.addPoint(point.image_coordinates)
            currentPolygonActor = self.MPRpoints.generatePolygonLastPoint(color=CFG.get_color('mpr-display-style'))
            self.panel_renderer.AddActor(currentPolygonActor)
        # self.presentPoints(self.MPRpoints, self.sliceIdx)

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
        _picker = vtk.vtkPropPicker()

        logging.info(f"Prop picked at {x}, {y} on slice {self.sliceIdx}.")

        if len(self.MPRpoints) == 0:
            print("no mpr points to edit")
        else:
            _distances = [(np.linalg.norm(np.array([x, y])-points[0:2]), points[0:2]) for points in self.MPRpoints]
            _distances.sort(key=lambda tup: tup[0], reverse=False)

            ic(_distances)

            _closest_point = _distances[0][1]

            ic(_closest_point)

            ic(_picker.PickProp(_closest_point[0], _closest_point[1], self.panel_renderer))

    def deleteAnnotation(self, x, y, prop):
        logging.debug("deleteAnnotation function activated")

        print(f'Deleting {prop} at {x}, {y}.')
        self.panel_renderer.RemoveActor(prop)

    def hide_off_slice_actors(self):
        ic(self.MPRpoints.displayed_points(self.sliceIdx))
        ic(self.MPRpoints.hidden_points(self.sliceIdx))

        for i in self.MPRpoints.hidden_points(self.sliceIdx):
            self.panel_renderer.RemoveActor(i.get_actor())
            self.window.Render()

    def render_panel(self):
        self.hide_off_slice_actors()
        print(f"new render in {self.sliceIdx}")

        ic(self.panel_renderer.GetActors().GetNumberOfItems())

        for i in self.MPRpoints.displayed_points(self.sliceIdx):
            self.panel_renderer.AddActor(i.get_actor())

            self.window.Render()

    def presentPoints(self, pointCollection, sliceIdx) -> None:
        logging.debug(f"{len(pointCollection)} points in memory on slice {sliceIdx}")

        self.hide_off_slice_actors()

        # ic(pointCollection.displayed_points(sliceIdx))
        #
        # ic([i.GetVisibility() for i in pointCollection.get_actor_list()])

        # if pointCollection.get_actor_list():
        #     for point in pointCollection.get_actor_list():
        #         ic(point.GetProperty())
        #         ic(point)
        #         self.panel_renderer.RemoveActor(point)
        #
        # for point in pointCollection.get_actor_list_for_slice(sliceIdx):
        #     self.panel_renderer.AddActor(point)  # TODO: all points are still shown
        #
        #     self.window.Render()

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
        self.render_panel()
        # self.presentPoints(self.MPRpoints, sliceIdx)

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

    def undoAnnotation(self):
        print('remove from display')

        logging.info(f"Removing last point, {len(self.MPRpoints)} MPR points")
        if len(self.MPRpoints) > 0:
            self.MPRpoints.delete(-1)
