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
from MRICenterline.Config import CFG
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

        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()

        self.level_val = self.imageData.level_value
        self.window_val = self.imageData.window_value

        self.sliceIdx = self.imageData.sliceIdx
        self.pastIndex = self.sliceIdx
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()

        self.window = self.interactor.GetRenderWindow()
        self.interactorStyle = interactorStyle
        self.reslice = vtkImageReslice()

        self.Cursor = vtkCursor2D()
        self.setCoordsText()

        self.connect_actor()

        self.MPRpoints = PointArray(point_color=(1, 0, 0),
                                    size=int(CFG.get_config_data('mpr-display-style', 'marker-size')),
                                    highlight_last=True,
                                    image=self.manager.imager)
        self.lengthPoints = PointArray(point_color=(0, 1, 0),
                                       size=int(CFG.get_config_data('length-display-style', 'marker-size')),
                                       image=self.manager.imager)
        self._point_order = []

        self.presentCursor()

        logging.debug("Rendering sequence")
        self.window.Render()

        # self._timer_status = "STOPPED"
        # self._start_time = None
        # self._stop_time = None
        # self._pause_time = None
        # self._resume_time = None
        # self.time_gap = []

    def connect_actor(self):
        self.reslice = vtk.vtkImageReslice()
        # self.reslice.SetInputData(self.imageData.get_vtk_data())
        self.reslice.SetInputData(self.imageData.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(self.imageData.transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

        self.panel_actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.panel_actor.GetProperty().SetColorWindow(self.window_val)
        self.panel_actor.GetProperty().SetColorLevel(self.level_val)

        self.panel_renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.panel_renderer.AddActor(self.panel_actor)
        self.panel_renderer.SetLayer(0)

        self.window.AddRenderer(self.panel_renderer)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.window.SetInteractor(self.interactor)
        self.panel_renderer.GetActiveCamera().ParallelProjectionOn()
        self.panel_renderer.ResetCamera()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.imageData.get_parallel_scale())

    def UpdateViewerMatrixCenter(self, center: List[int], sliceIdx):
        matrix = self.reslice.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(1 + self.imageData.size[2] - sliceIdx))
        self.window.Render()
        self.sliceIdx = sliceIdx
        self.imageData.sliceIdx = sliceIdx
        self.manager.updateSliderIndex(self.sliceIdx)
        self.render_panel()

    def Start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    def render_panel(self):
        logging.debug(f"Rendering slice: {self.sliceIdx} / ITK zindex: {1 + self.imageData.size[2] - self.sliceIdx}")
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

    ######################################################################
    #                             text actors                            #
    ######################################################################

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
        self.textActorWindow.SetInput("Window: " + str(self.window_val))
        self.panel_renderer.AddActor(self.textActorWindow)

    def setCoordsText(self):
        _display_color = CFG.get_color('display')
        _window_size = self.window.GetSize()

        self.textActorCoords = vtkTextActor()
        self.textActorCoords.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.textActorCoords.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorCoords.SetInput(" ")

        self.textActorCoords.SetDisplayPosition(0, 4*int(CFG.get_config_data('display', 'font-size')))

        self.panel_renderer.AddActor(self.textActorCoords)

    def setLevelText(self):
        _display_color = CFG.get_color('display')
        _order = CONST.ORDER_OF_CONTROLS.index('Level')

        self.textActorLevel = vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.textActorLevel.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorLevel.SetDisplayPosition(0, _order*int(CFG.get_config_data('display', 'font-size')))
        self.textActorLevel.SetInput("Level: " + str(self.level_val))
        self.panel_renderer.AddActor(self.textActorLevel)

    def updateDisplayedCoords(self, coords):
        try:
            self.textActorCoords.SetInput(f'x: {round(coords[0], 2)}, y: {round(coords[1], 2)}, z: {round(coords[2], 2)}')
        except TypeError:  # it's out of bounds
            pass
        self.window.Render()

    ######################################################################
    #                          callback functions                        #
    ######################################################################

    def adjustWindow(self, window: int):
        self.panel_actor.GetProperty().SetColorWindow(window)
        self.window_val = window
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.window_val)))
        self.window.Render()

    def adjustLevel(self, level: int):
        self.panel_actor.GetProperty().SetColorLevel(level)
        self.level_val = level
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.level_val)))
        self.window.Render()

    def updateWindowLevel(self):
        logging.debug(f"Window and Level updated to ({self.panel_actor.GetProperty().GetColorWindow()}, {self.panel_actor.GetProperty().GetColorLevel()})")
        self.manager.changeWindow(self.panel_actor.GetProperty().GetColorWindow())
        self.manager.changeLevel(self.panel_actor.GetProperty().GetColorLevel())

    def updateZoomFactor(self):
        curParallelScale = self.panel_renderer.GetActiveCamera().GetParallelScale()
        newZoomFactor = curParallelScale / self.imageData.get_parallel_scale()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.imageData.get_parallel_scale() * newZoomFactor)
        self.window.Render()

    def moveBullsEye(self, newCoordinates):
        self.Cursor.SetFocalPoint(newCoordinates)
        self.window.Render()

    ######################################################################
    #                          point processing                          #
    ######################################################################

    def addPoint(self, pointType, pickedCoordinates):
        logging.debug(f"Adding {pointType} point in {pickedCoordinates}")

        self._point_order.append(pointType.upper())
        if pointType.upper() == "MPR":
            self.processNewPoint(self.MPRpoints, pickedCoordinates)
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, pickedCoordinates)

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
                print(key, val, _loader.slide_indices[key])

        # if 'length points' in _loader.point_set.keys():
        #     logging.debug(f"Loading {len(_loader.point_set['length points'].points)} length points")
        #     for key, val in enumerate(_loader.point_set['length points'].points):
        #         self.loadPoint("LENGTH", val, _loader.slide_indices[key])

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

    def setSliceIndex(self, index: int):
        self.reslice.Update()
        sliceSpacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, (index-self.pastIndex)*sliceSpacing, 1))
        if 1 <= index <= self.imageData.size[2]:
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

        # sliceIdx = np.int(np.round((center[2] - self.imageData.origin[2]) / self.imageData.spacing[2] - 0.5))
        sliceIdx = np.int(1 + (np.round(((center[2] - self.imageData.origin[2]) / self.imageData.spacing[2]))))

        if 1 <= sliceIdx <= self.imageData.size[2]:
            self.pastIndex = sliceIdx
            self.UpdateViewerMatrixCenter(center, sliceIdx)

    ######################################################################
    #                        save / timer functions                      #
    ######################################################################

    def save_points(self, time_elapsed):
        """
        SaveFormatter is initialized here so that it has access to the MRI and length points arrays,
        and then it's passed to CaseModel so that it has access to the timers and the case ID
        """
        sf = SaveFormatter(parent=self, imager=self.manager.imager)
        sf.set_time_gap(time_elapsed)
        sf.save()

        # _save_formatter = SaveFormatter(imagedata=self.imageData, path=self.imageData.path)
        # if len(self.lengthPoints) + len(self.MPRpoints):
        #     if len(self.lengthPoints):
        #         _save_formatter.add_pointcollection_data('length points', self.lengthPoints)
        #         if len(self.lengthPoints) > 2:
        #             logging.debug(f"Also saving total length: {self.lengthPoints.total_length}")
        #             _save_formatter.add_generic_data('measured length', self.lengthPoints.total_length)
        #
        #     if len(self.MPRpoints):
        #         _save_formatter.add_pointcollection_data("MPR points", self.MPRpoints)
        #     logging.info(f"Saved {len(self.lengthPoints) + len(self.MPRpoints)} points to data folder")
        #
        #     _save_formatter.add_timestamps(self._start_time, self._stop_time, self.time_gap)
        #     _save_formatter.save_data()



    # def start_timer(self):
    #     self._timer_status = "STARTED"
    #
    #     self._start_time = datetime.now(timezone.utc).astimezone()
    #     logging.info(f"Starting timer: {self._start_time}")
    #
    # def stop_timer(self):
    #     self._timer_status = "STOPPED"
    #
    #     self._stop_time = datetime.now(timezone.utc).astimezone()
    #     logging.info(f"Stopping timer: {self._stop_time}")
    #
    #     if self._timer_status == "RESUMED":
    #         self.resume_timer()
    #
    #     if self.time_gap:
    #         logging.info(f"Time measured: {self._stop_time - self._start_time - sum(self.time_gap, timedelta())}")
    #     else:
    #         logging.info(f"Time measured: {self._stop_time - self._start_time}")
    #
    # def pause_timer(self):
    #     self._timer_status = "PAUSED"
    #
    #     self._pause_time = datetime.now(timezone.utc).astimezone()
    #     logging.info(f"Pausing timer: {self._pause_time}")
    #
    # def resume_timer(self):
    #     self._timer_status = "RESUMED"
    #
    #     self._resume_time = datetime.now(timezone.utc).astimezone()
    #     logging.info(f"Resuming timer: {self._resume_time}")
    #
    #     logging.info(f"Time gap: {self._resume_time - self._pause_time}")
    #     self.time_gap.append(self._resume_time - self._pause_time)

    ######################################################################
    #                         annotation functions                       #
    ######################################################################

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
