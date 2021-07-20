from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from typing import Tuple
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QFileDialog
from PyQt5.Qt import *

from MRICenterline.DisplayPanel.View.Toolbar import DisplayPanelToolbar
from MRICenterline.DisplayPanel.Model.GenericViewerManager import GenericViewerManager
from MRICenterline.DisplayPanel.View.SlidersLayout import SlidersLayout
from MRICenterline.DisplayPanel.Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from MRICenterline.DisplayPanel.Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle

from MRICenterline.Interface import DisplayCenterlineInterface
from MRICenterline.CenterlinePanel import CenterlinePanel

from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG
import logging
logging.getLogger(__name__)


class GenericModel(QWidget):
    def __init__(self, MRIimages):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.toolbar = DisplayPanelToolbar(parent=self, manager=self)
        # self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False
        self.interface = DisplayCenterlineInterface()

        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.widgets = SequenceInteractorWidgets(MRIimages.get_sequences(), self)

        self.sequenceManager = GenericViewerManager(self, MRIimages)
        self.view = self.sequenceManager.loadSequence(0, self.interactor, self.interactorStyle)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider,
                                      levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)

#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

    def initializeSliderValues(self):
        logging.info(f"Index value {int(self.view.sliceIdx)}")
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5],
                               windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

        self.interface.initialize_level_window(level=self.view.LevelVal, window=self.view.WindowVal)

#_____________________________________________Interface to Widgets_____________________________________________________

    def changeSequence(self, sequenceIndex: int):
        logging.info(f"Sequence changed {sequenceIndex}")
        try:
            self.view = self.sequenceManager.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
            self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))
        except Exception as err:
            logging.critical(f"Error: {err}")

    def setListWidgetIndex(self, index):
        # sets index of sequences in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.view.adjustWindow(window)
        self.interface.set_window(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.view.adjustLevel(level)
        self.interface.set_level(level)

    def setIndex(self, index: int):
        logging.info(f"Set index {int(index)}")
        self.view.setSliceIndex(index)

    def updateSliderIndex(self, index):
        self.widgets.indexSlider.setValue(index)

    def showCenterlinePanel(self):
        if self.view.MPRpoints.getCoordinatesArray().shape[0] <= 3:
            MSG.msg_box_warning("Not enough points clicked to calculate Centerline")
        else:
            logging.info("Opening Centerline Panel dockable widget")
            self.interface.initialize_points(self.view.MPRpoints.getCoordinatesArray())

            _centerline_panel = CenterlinePanel(image=self.view.imageData, interface=self.interface,
                                                parent=self)
            self.layout.addWidget(_centerline_panel)
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

    def showPatientInfoTable(self):
        print("show patient info table")