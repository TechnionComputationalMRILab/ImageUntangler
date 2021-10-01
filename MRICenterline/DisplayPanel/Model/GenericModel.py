from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from typing import Tuple
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFileDialog, QShortcut
from PyQt5.Qt import QSizePolicy
from PyQt5.QtGui import QKeySequence

from MRICenterline.DisplayPanel.View.Toolbar import DisplayPanelToolbar
from MRICenterline.DisplayPanel.Model.GenericViewerManager import GenericViewerManager
from MRICenterline.DisplayPanel.View.SlidersAndSpinboxLayout import SlidersAndSpinboxLayout
from MRICenterline.DisplayPanel.Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle

from MRICenterline.Interface import DisplayCenterlineInterface
from MRICenterline.CenterlinePanel import CenterlinePanel

from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class GenericModel(QWidget):
    def __init__(self, MRIimages, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.toolbar = DisplayPanelToolbar(parent=self, manager=self)

        self.statusbar = parent.parent().parent().parent().parent().statusBar() # TODO: thanks i hate it

        # self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False
        self.interface = DisplayCenterlineInterface()

        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.interactor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.widgets = SequenceInteractorWidgets(MRIimages.get_sequences(), self)

        self.sequenceManager = GenericViewerManager(self, MRIimages)
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

    def saveLengths(self):
        logging.info("Saving lengths to file...")
        # first argument of qfiledialog needs to be the qwidget itself
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Length Points As", CFG.get_config_data("folders", 'default-save-to-folder'),
                "%s Files (*.%s)" % ("json".upper(), "json"))

        if fileName:
            self.view.saveLengths(fileName)
            logging.info(f"Saved as {fileName}")

    def saveMPRPoints(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save MPR Points As", CFG.get_config_data("folders", 'default-save-to-folder'),
                "%s Files (*.%s);;All Files (*)" % ("json".upper(), "json"))

        if fileName:
            self.view.saveMPRPoints(fileName)

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
        MSG.msg_box_info("Patient info display not implemented in this version.")

# _________________________________________Keyboard Shortcuts_______________________________________

    def set_up_keyboard_shortcuts(self):
        self.undo_kb_shortcut = QShortcut(QKeySequence('Ctrl+z'), self)
        self.undo_kb_shortcut.activated.connect(self.undo_kb_shortcut_func)

    def undo_kb_shortcut_func(self):
        logging.info("Undo keyboard shortcut used")
        self.view.undoAnnotation()
