import numpy as np
from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D
import vtkmodules.all as vtk
from datetime import datetime, timezone, timedelta

from MRICenterline.Points import PointArray
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MRICenterline.Loader.LoadPoints import LoadPoints
from MRICenterline.Points.SaveFormatter import SaveFormatter

from MRICenterline.utils import message as MSG
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class GenericSequenceViewer:
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor,
                 interactorStyle: SequenceViewerInteractorStyle, image):
        self.count = 0
        self.manager = manager
        self.interactor = interactor
        self.imageData = image
        self.z_coords = self.imageData.z_coords
        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()

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

        self.Cursor = vtkCursor2D()
        self.performReslice()
        self.connectActor()
        self.renderImage()

        self.MPRpoints = PointArray(point_color=(1, 0, 0),
                                    size=int(CFG.get_config_data('mpr-display-style', 'marker-size')),
                                    highlight_last=True)
        self.lengthPoints = PointArray(point_color=(0, 1, 0),
                                       size=int(CFG.get_config_data('length-display-style', 'marker-size')))
        self._point_order = []

        self.presentCursor()

        logging.debug("Rendering sequence")
        self.window.Render()

        self._timer_status = "STOPPED"
        self._start_time = None
        self._stop_time = None
        self._pause_time = None
        self._resume_time = None
        self._time_gap = []

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

    def processNewPoint(self, pointCollection, pickedCoordinates):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], self.sliceIdx]  # x,y,z,sliceIdx
        pointCollection.add_point(pointLocation)
        self.panel_renderer.AddActor(pointCollection[-1].actor)
        self.render_panel()

    def loadAllPoints(self, filename):
        _loader = LoadPoints(filename, self.imageData)
        logging.info(f'Loading {len(_loader.point_set.keys())} point sets from file')

        if 'MPR points' in _loader.point_set.keys():
            logging.debug(f"Loading {len(_loader.point_set['MPR points'].points)} MPR points")
            for key, val in enumerate(_loader.point_set['MPR points'].points):
                self.loadPoint("MPR", val, _loader.slide_indices[key])
        if 'length points' in _loader.point_set.keys():
            logging.debug(f"Loading {len(_loader.point_set['length points'].points)} length points")
            for key, val in enumerate(_loader.point_set['length points'].points):
                self.loadPoint("LENGTH", val, _loader.slide_indices[key])

    def processLoadedPoint(self, pointCollection, pickedCoordinates, sliceIdx):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], sliceIdx]  # x,y,z,sliceIdx
        pointCollection.add_point(pointLocation)
        self.panel_renderer.AddActor(pointCollection[-1].actor)
        self.render_panel()

    def loadPoint(self, pointType, pickedCoordinates, slideIdx):
        logging.debug(f"Loading {pointType} point in {pickedCoordinates}")

        self._point_order.append(pointType.upper())
        if pointType.upper() == "MPR":
            self.processLoadedPoint(self.MPRpoints, pickedCoordinates, slideIdx)
        elif pointType.upper() == "LENGTH":
            self.processLoadedPoint(self.lengthPoints, pickedCoordinates, slideIdx)

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
        logging.debug(f"Adding {pointType} point in {pickedCoordinates}")

        self._point_order.append(pointType.upper())
        if pointType.upper() == "MPR":
            self.processNewPoint(self.MPRpoints, pickedCoordinates)
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, pickedCoordinates)

    def calculateLengths(self):
        # TODO: remove this, use length actors instead
        # pointsPositions = np.asarray(self.lengthPoints.get_coordinates_as_array())
        # allLengths = [np.linalg.norm(pointsPositions[j, :] - pointsPositions[j + 1, :]) for j in
        #               range(len(pointsPositions) - 1)]
        #
        # totalDistance = np.sum(allLengths)

        allLengths = self.lengthPoints.lengths
        totalDistance = self.lengthPoints.total_length

        strdis = ["{0:.2f}".format(allLengths[i]) for i in range(len(allLengths))]

        MSG.msg_box_info("Calculated length",
                         info="The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),"{0:.2f}".format(totalDistance)))

    def save_points(self):
        logging.info('Saving file...')

        _save_formatter = SaveFormatter(imagedata=self.imageData, path=self.imageData.path)
        print("1")
        if len(self.lengthPoints) + len(self.MPRpoints):
            print("2")
            if len(self.lengthPoints):
                print("3")
                _save_formatter.add_pointcollection_data('length points', self.lengthPoints)
                if len(self.lengthPoints) > 2:
                    logging.debug(f"Also saving total length: {self.lengthPoints.total_length}")
                    _save_formatter.add_generic_data('measured length', self.lengthPoints.total_length)

            if len(self.MPRpoints):
                _save_formatter.add_pointcollection_data("MPR points", self.MPRpoints)
            logging.info(f"Saved {len(self.lengthPoints) + len(self.MPRpoints)} points to data folder")

            _save_formatter.add_timestamps(self._start_time, self._stop_time, self._time_gap)
            _save_formatter.save_data()

    def modifyAnnotation(self, x, y):
        _picker = vtk.vtkPropPicker()

        logging.info(f"Prop picked at {x}, {y} on slice {self.sliceIdx}.")

        if len(self.MPRpoints) == 0:
            print("no mpr points to edit")
        else:
            _distances = [(np.linalg.norm(np.array([x, y])-points[0:2]), points[0:2]) for points in self.MPRpoints]
            _distances.sort(key=lambda tup: tup[0], reverse=False)
            _closest_point = _distances[0][1]

    def deleteAnnotation(self, x, y, prop):
        logging.debug("deleteAnnotation function activated")

        print(f'Deleting {prop} at {x}, {y}.')
        self.panel_renderer.RemoveActor(prop)

    def render_panel(self):
        _zcoord = round(self.z_coords[self.sliceIdx], 2)
        logging.debug(f"Rendering slice {self.sliceIdx} / z = {_zcoord}")
        logging.debug(f"Current number of actors: {self.panel_renderer.GetActors().GetNumberOfItems()}")

        for i in self.lengthPoints:
            i.set_visibility(i.slice_idx == self.sliceIdx)

        if self.MPRpoints.hiding_intermediate_points:
            _first_point = self.MPRpoints.get_first_point()
            _first_point.set_visibility(_first_point.slice_idx == self.sliceIdx)

            _last_point = self.MPRpoints.get_last_point()
            _last_point.set_visibility(_last_point.slice_idx == self.sliceIdx)
        else:
            for i in self.MPRpoints:
                i.set_visibility(i.slice_idx == self.sliceIdx)

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
        self.render_panel()

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

    def start_timer(self):
        self._timer_status = "STARTED"

        self._start_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Starting timer: {self._start_time}")

    def stop_timer(self):
        self._timer_status = "STOPPED"

        self._stop_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Stopping timer: {self._stop_time}")

        if self._timer_status == "RESUMED":
            self.resume_timer()

        if self._time_gap:
            logging.info(f"Time measured: {self._stop_time - self._start_time - sum(self._time_gap, timedelta())}")
        else:
            logging.info(f"Time measured: {self._stop_time - self._start_time}")

    def pause_timer(self):
        self._timer_status = "PAUSED"

        self._pause_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Pausing timer: {self._pause_time}")

    def resume_timer(self):
        self._timer_status = "RESUMED"

        self._resume_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Resuming timer: {self._resume_time}")

        logging.info(f"Time gap: {self._resume_time - self._pause_time}")
        self._time_gap.append(self._resume_time - self._pause_time)

    def undoAnnotation(self):
        logging.info(f"Removing last {self._point_order[-1]} point")

        if self._point_order[-1] == "MPR":
            if len(self.MPRpoints) > 0:
                self.MPRpoints.delete(-1)
        elif self._point_order[-1] == "LENGTH":
            if len(self.lengthPoints) > 0:
                self.lengthPoints.delete(-1)
        self._point_order.pop()
        self.window.Render()

    def deleteAllPoints(self):
        logging.info("Removing all points")

        while len(self.MPRpoints) > 0:
            self.MPRpoints.delete(-1)

        while len(self.lengthPoints) > 0:
            self.lengthPoints.delete(-1)

        self.window.Render()

    def show_intermediate_points(self):
        logging.debug("Show intermediate MPR points (i.e., show all points)")
        self.MPRpoints.hiding_intermediate_points = False
        self.MPRpoints.show_intermediate_points()
        # self.window.Render()
        self.render_panel()

    def hide_intermediate_points(self):
        logging.info("Hiding intermediate MPR points")
        self.MPRpoints.hiding_intermediate_points = True
        self.MPRpoints.hide_intermediate_points()
        # self.window.Render()
        self.render_panel()

    # TODO REMOVE AFTER COMPLETION
    def convert_zcoords(self):
        print("CONVERTING")

        from MRICenterline.utils import annotation_cleaner

        _zlist = []
        for i in range(self.imageData.extent[5]):
            self.setSliceIndex(i)

            matrix = self.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            __zCoordinate = (center[2] - self.imageData.origin[2]) - self.imageData.dimensions[2] \
                            * self.imageData.spacing[2] / 2

            _zlist.append(__zCoordinate)

        # annotation_cleaner.convert(self.imageData, _zlist, self.manager.manager)
        return _zlist

    # TODO REMOVE AFTER COMPLETION
    def run_cleaner(self):
        print("CONVERTING")

        from MRICenterline.utils import annotation_cleaner

        _zlist = []
        for i in range(self.imageData.extent[5]):
            self.setSliceIndex(i)

            matrix = self.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            __zCoordinate = (center[2] - self.imageData.origin[2]) - self.imageData.dimensions[2] \
                            * self.imageData.spacing[2] / 2

            _zlist.append(__zCoordinate)

        annotation_cleaner.convert(self.imageData, _zlist, self.manager.manager)
