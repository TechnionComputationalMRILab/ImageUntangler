from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import numpy as np
from typing import Tuple
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFileDialog, QShortcut
from PyQt5.Qt import QSizePolicy
from PyQt5.QtGui import QKeySequence

from MRICenterline.DisplayPanel.Model.GenericViewerManager import GenericViewerManager
from MRICenterline.DisplayPanel.Model.Imager import Imager

from MRICenterline.DisplayPanel.View.Toolbar import DisplayPanelToolbar
from MRICenterline.DisplayPanel.View.SlidersAndSpinboxLayout import SlidersAndSpinboxLayout

from MRICenterline.DisplayPanel.Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MRICenterline.PatientInfo import PatientInfoPanel

from MRICenterline.FileManipulation import DisplayPanel as DPFileManip

from MRICenterline.Interface import DisplayCenterlineInterface
from MRICenterline.CenterlinePanel import CenterlinePanel

from MRICenterline.Config import CFG
from MRICenterline.utils import message as MSG
from MRICenterline.utils import Timer

import logging
logging.getLogger(__name__)


class GenericModel(QWidget):
    def __init__(self, images: Imager, parent, use_sequence):
        super().__init__(parent)
        self.use_sequence = use_sequence
        self.images = images
        self.interface = DisplayCenterlineInterface()
        self.timer = Timer()
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False
        self.statusbar = parent.parent().parent().parent().parent().statusBar()  # TODO: thanks i hate it

        self.layout = QVBoxLayout(self)
        self.toolbar = DisplayPanelToolbar(parent=self, manager=self)

        self.set_up_display_panel()
        self.set_up_sliders()
        self.set_up_keyboard_shortcuts()

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.widgets.sequenceList)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(self.sliderspinboxLayout)

    def set_up_display_panel(self):

        def build_frame():
            """ creates a maximized frame for the QVTK Window"""
            _frame = QGroupBox()
            _frame.showMaximized()
            return _frame

        frame = build_frame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.interactor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.widgets = SequenceInteractorWidgets(self.images.get_sequences(), self)
        self.sequenceManager = GenericViewerManager(self, self.images)

        if self.use_sequence in self.images.get_sequences():
            self.current_sequence = -1
            logging.debug(f"Loading single image using sequence {self.use_sequence}")
            _index = self.images.get_sequences().index(self.use_sequence)
            self.view = self.sequenceManager.load_single_sequence(self.interactor, self.interactorStyle,
                                                                  self.images[_index], _index)
            self.widgets.freeze_sequence_list(self.use_sequence)
        else:
            logging.debug("Loading multiple sequences...")
            self.current_sequence = 0
            self.view = self.sequenceManager.loadSequence(self.current_sequence, self.interactor,
                                                          self.interactorStyle)

        self.sliderspinboxLayout = SlidersAndSpinboxLayout(window_widgets=self.widgets.window_widgets,
                                                           level_widgets=self.widgets.level_widgets,
                                                           index_widgets=self.widgets.index_widgets)

    def set_up_sliders(self):
        self.widgets.initialize_values(slice_index=int(self.view.sliceIdx), max_slice=self.view.imageData.size[2],
                                       window_value=int(self.view.window_val), level_value=int(self.view.level_val))

    ###########################################################################
    #                             widget functions                            #
    ###########################################################################

    def changeSequence(self, sequenceIndex: int):
        logging.info(f"Sequence changed {sequenceIndex}")
        self.statusbar.update_memory_usage()
        try:
            self.view = self.sequenceManager.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
            self.widgets.initialize_values(slice_index=int(self.view.sliceIdx), max_slice=self.view.imageData.size[2],
                                           window_value=int(self.view.window_val), level_value=int(self.view.level_val))
        except Exception as err:
            logging.critical(f"Error: {err}")
        else:
            if self.current_sequence >= 0:
                self.current_sequence = sequenceIndex

    def setListWidgetIndex(self, index):
        # sets index of sequences in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.window_widgets['Slider'].setValue(window)
        self.widgets.window_widgets['Spinbox'].setValue(window)
        self.view.adjustWindow(window)
        self.interface.set_window(window)

    def changeLevel(self, level: int):
        self.widgets.level_widgets['Slider'].setValue(level)
        self.widgets.level_widgets['Spinbox'].setValue(level)
        self.view.adjustLevel(level)
        self.interface.set_level(level)

    def setIndex(self, index: int):
        logging.info(f"Set index {int(index)}")
        self.view.setSliceIndex(index)

    def updateSliderIndex(self, index):
        self.widgets.index_widgets['Slider'].setValue(index)
        self.widgets.index_widgets['Spinbox'].setValue(index)

    def showCenterlinePanel(self):
        if self.view.MPRpoints.get_coordinates_as_array().shape[0] <= 3:
            MSG.msg_box_warning("Not enough points clicked to calculate Centerline")
        else:
            logging.info("Opening Centerline Panel dockable widget")
            print(self.view.MPRpoints.get_coordinates_as_array())
            self.interface.initialize_points(self.view.MPRpoints.get_coordinates_as_array())
            self.interface.set_level(self.view.level_val)
            self.interface.set_window(self.view.window_val)

            self.centerline_panel = CenterlinePanel(image=self.view.imageData, interface=self.interface,
                                                    parent=self)
            self.layout.addWidget(self.centerline_panel)

    ###########################################################################
    #                         interactor callbacks                            #
    ###########################################################################

    def moveBullsEye(self, coordinates: Tuple[int]):
        self.view.moveBullsEye(coordinates)

    def updateWindowLevel(self):
        self.view.updateWindowLevel()

    def updateZoomFactor(self):
        self.view.updateZoomFactor()

    def updateDisplayedCoords(self, coords):
        self.view.updateDisplayedCoords(coords)

    def clearCursor(self):
        self.view.Cursor.AllOff()
        self.view.window.Render()

    def addCursor(self):
        self.view.Cursor.AllOff()
        self.view.Cursor.AxesOn()
        self.view.window.Render()

    def changeSliceIndex(self, changeFactor: int):
        self.view.adjustSliceIdx(changeFactor)
        self.widgets.indexSlider.setValue(self.view.sliceIdx)

    def addPoint(self, pointType: str, pickedCoordinates: Tuple[int]):
        self.view.addPoint(pointType, pickedCoordinates)

    ###########################################################################
    #                            toolbar functions                            #
    ###########################################################################

    def reverseMPRpointsStatus(self):
        # self.interactorStyle.actions["PickingMPR"] = int(not self.interactorStyle.actions["PickingMPR"])
        self.interactorStyle.actions["PickingMPR"] = 1

    def reverseLengthPointsStatus(self):
        # self.interactorStyle.actions["PickingLength"] = int(not self.interactorStyle.actions["PickingLength"])
        self.interactorStyle.actions["PickingLength"] = 1

    def calculateLengths(self):
        self.view.calculateLengths()

    def save_all(self):
        logging.info('Saving annotations to database...')
        self.view.save_points(time_elapsed=self.timer.get_total_time_elapsed())

    def loadAllPoints(self, filename):
        logging.debug(f"Opening points from {filename}")
        self.view.loadAllPoints(filename)

    def disablePointPicker(self):
        self.interactorStyle.actions["PickingMPR"] = 0
        self.interactorStyle.actions["PickingLength"] = 0

    def drawLengthLines(self):
        self.view.drawLengthLines()

    def drawMPRSpline(self):
        self.view.drawMPRSpline()

    def showMPRPanel(self):
        self.view.showMPRPanel()

    def modifyAnnotation(self, x, y):
        self.view.modifyAnnotation(x, y)

    def deleteAnnotation(self, x, y, prop):
        self.view.deleteAnnotation(x, y, prop)

    def undoAnnotation(self):
        self.view.undoAnnotation()

    def deleteAllPoints(self):
        self.view.deleteAllPoints()

    def showPatientInfoTable(self):
        logging.info("Showing patient table")
        _patient_info_panel = PatientInfoPanel(parent=self)
        self.layout.addWidget(_patient_info_panel)
        _patient_info_panel.show()

    def show_intermediate_points(self):
        self.view.show_intermediate_points()

    def hide_intermediate_points(self):
        self.view.hide_intermediate_points()

    def export_one_sequence(self):
        logging.info(f"Exporting {self.images.get_sequences()[self.sequenceManager.seq_idx]}...")
        file_list = self.images.get_files(self.images.get_sequences()[self.sequenceManager.seq_idx])
        DPFileManip.export_single_sequence(file_list)

    def export_seq_and_pts(self):
        pass

    ###########################################################################
    #                              timer functions                            #
    ###########################################################################

    def start_timer(self):
        self.timer.start_timer()

    def stop_timer(self):
        self.timer.stop_timer()

    def pause_timer(self):
        self.timer.pause_timer()

    def resume_timer(self):
        self.timer.resume_timer()

    ###########################################################################
    #                           keyboard shortcuts                            #
    ###########################################################################

    def set_up_keyboard_shortcuts(self):
        _undo_kb_shortcut = QShortcut(QKeySequence('Ctrl+z'), self)
        _undo_kb_shortcut.activated.connect(lambda : logging.info("Undo keyboard shortcut used"))
        _undo_kb_shortcut.activated.connect(self.view.undoAnnotation)

        _save_kb_shortcut = QShortcut(QKeySequence('Ctrl+s'), self)
        _save_kb_shortcut.activated.connect(lambda : logging.info("Save keyboard shortcut used"))
        _save_kb_shortcut.activated.connect(self.save_all)
