from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import numpy as np
from typing import Tuple
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFileDialog, QShortcut
from PyQt5.Qt import QSizePolicy
from PyQt5.QtGui import QKeySequence

from MRICenterline.DisplayPanel.View.Toolbar import DisplayPanelToolbar
from MRICenterline.DisplayPanel.Model.GenericViewerManager import GenericViewerManager
from MRICenterline.DisplayPanel.View.SlidersAndSpinboxLayout import SlidersAndSpinboxLayout
from MRICenterline.DisplayPanel.Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MRICenterline.PatientInfo import PatientInfoPanel

from MRICenterline.Interface import DisplayCenterlineInterface
from MRICenterline.CenterlinePanel import CenterlinePanel

from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class GenericModel(QWidget):
    def __init__(self, MRIimages, parent, use_sequence):
        super().__init__(parent)
        self.images = MRIimages

        self.layout = QVBoxLayout(self)
        self.toolbar = DisplayPanelToolbar(parent=self, manager=self)

        self.statusbar = parent.parent().parent().parent().parent().statusBar()  # TODO: thanks i hate it

        # self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False
        self.interface = DisplayCenterlineInterface()

        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.interactor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.widgets = SequenceInteractorWidgets(self.images.get_sequences(), self)
        self.sequenceManager = GenericViewerManager(self, self.images)

        if use_sequence in self.images.get_sequences():
            logging.debug(f"Loading single image using sequence {use_sequence}")
            _index = self.images.get_sequences().index(use_sequence)
            self.view = self.sequenceManager.load_single_sequence(self.interactor, self.interactorStyle, self.images[_index])
            self.widgets.freeze_sequence_list(use_sequence)
        else:
            logging.debug("Loading multiple sequences...")
            self.view = self.sequenceManager.loadSequence(0, self.interactor, self.interactorStyle)

        self.sliderspinboxLayout = SlidersAndSpinboxLayout(window_widgets=self.widgets.window_widgets,
                                                           level_widgets=self.widgets.level_widgets,
                                                           index_widgets=self.widgets.index_widgets)

        self.set_up_sliders()
        self.set_up_keyboard_shortcuts()

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.widgets.sequenceList)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(self.sliderspinboxLayout)

        # self.view.convert_zcoords()

#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

    def set_up_sliders(self):
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice=self.view.imageData.extent[5],
                               windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

#_____________________________________________Interface to Widgets_____________________________________________________

    def changeSequence(self, sequenceIndex: int):
        logging.info(f"Sequence changed {sequenceIndex}")
        self.statusbar.update_memory_usage()
        try:
            self.view = self.sequenceManager.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
            self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice=self.view.imageData.extent[5],
                                   windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))
        except Exception as err:
            logging.critical(f"Error: {err}")

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
            self.interface.set_level(self.view.LevelVal)
            self.interface.set_window(self.view.WindowVal)

            self.centerline_panel = CenterlinePanel(image=self.view.imageData, interface=self.interface,
                                                    parent=self)
            self.layout.addWidget(self.centerline_panel)

#__________________________________________ Interface to InteractorStyle ________________________________

    def moveBullsEye(self, coordinates: Tuple[int]):
        self.view.moveBullsEye(coordinates)

    def updateWindowLevel(self):
        self.view.updateWindowLevel()

    def updateZoomFactor(self):
        self.view.updateZoomFactor()

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

#________________________________________Interface to Toolbar_____________________________________
    def reverseMPRpointsStatus(self):
        # self.interactorStyle.actions["PickingMPR"] = int(not self.interactorStyle.actions["PickingMPR"])
        self.interactorStyle.actions["PickingMPR"] = 1

    def reverseLengthPointsStatus(self):
        # self.interactorStyle.actions["PickingLength"] = int(not self.interactorStyle.actions["PickingLength"])
        self.interactorStyle.actions["PickingLength"] = 1

    def calculateLengths(self):
        self.view.calculateLengths()

    # def calculateMPR(self):
    #     self.view.calculateMPR()

    def save_all(self):
        self.view.save_points()

    # def saveLengths(self):
    #     logging.info("Saving lengths to file...")
    #     # first argument of qfiledialog needs to be the qwidget itself
    #     # fileName, _ = QFileDialog.getSaveFileName(self, "Save Length Points As", CFG.get_config_data("folders", 'default-save-to-folder'),
    #     #         "%s Files (*.%s)" % ("json".upper(), "json"))
    #     #
    #     # if fileName:
    #     self.view.saveLengths()
    #     # logging.info(f"Saved as {fileName}")
    #
    # def saveMPRPoints(self):
    #     self.view.saveMPRPoints()

    def loadAllPoints(self, filename):
        logging.debug(f"Opening points from {filename}")
        self.view.loadAllPoints(filename)

    def loadLengthPoints(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Load length points")
        if fileName:
            logging.info(f"Loading length points from {fileName}")
            self.view.loadLengthPoints(fileName)

    def loadMPRPoints(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Load MPR points")
        if fileName:
            logging.info(f"Loading MPR points from {fileName}")
            self.view.loadMPRPoints(fileName)

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
        # _patient_info_panel = PatientInfoPanel(parent=self)
        # self.layout.addWidget(_patient_info_panel)

    def start_timer(self):
        self.view.start_timer()

    def stop_timer(self):
        self.view.stop_timer()

    def pause_timer(self):
        self.view.pause_timer()

    def resume_timer(self):
        self.view.resume_timer()

    def show_intermediate_points(self):
        self.view.show_intermediate_points()

    def hide_intermediate_points(self):
        self.view.hide_intermediate_points()

# _________________________________________Keyboard Shortcuts_______________________________________

    def set_up_keyboard_shortcuts(self):
        _undo_kb_shortcut = QShortcut(QKeySequence('Ctrl+z'), self)
        _undo_kb_shortcut.activated.connect(lambda : logging.info("Undo keyboard shortcut used"))
        _undo_kb_shortcut.activated.connect(self.view.undoAnnotation)

        _save_kb_shortcut = QShortcut(QKeySequence('Ctrl+s'), self)
        _save_kb_shortcut.activated.connect(lambda : logging.info("Save keyboard shortcut used"))
        _save_kb_shortcut.activated.connect(self.save_all)

    # TODO REMOVE
    def FIXER(self):
        _zlist = self.view.convert_zcoords()
        _coords = np.copy(self.view.MPRpoints.get_coordinates_as_array())

        _slice_index_based = self.view.z_coords

        # print(_coords)

        _list = []
        for pt in _coords:
            for k, bad_z in enumerate(_slice_index_based):
                if np.isclose(pt[2], bad_z):
                    print(f"replace {bad_z} with {_zlist[k]}")
                    _list.append(_zlist[k])
                    break

        print(_coords.shape)
        print(np.array(_list).shape)

        _coords[:, 2] = np.array(_list)

        print(_coords)

        self.interface.initialize_points(_coords)
        self.interface.set_level(self.view.LevelVal)
        self.interface.set_window(self.view.WindowVal)
        print(self.interface.level)

        self.centerline_panel = CenterlinePanel(image=self.view.imageData, interface=self.interface,
                                                parent=self)
        self.layout.addWidget(self.centerline_panel)

    def FIXER2(self):
        self.view.run_cleaner()