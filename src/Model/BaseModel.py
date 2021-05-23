from typing import Tuple
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QFileDialog
from View.Toolbar import Toolbar

from util import config_data, stylesheets, logger
logger = logger.get_logger()


class BaseModel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.toolbar = Toolbar(parent=self, manager=self)
        self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False

#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

#_____________________________________________Interface to Widgets_____________________________________________________

    def changeSequence(self, sequenceIndex: int):
        raise NotImplementedError

    def setListWidgetIndex(self, index):
        # sets index of sequences in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.view.adjustWindow(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.view.adjustLevel(level)

    def setIndex(self, index: int):
        raise NotImplementedError

    def updateSliderIndex(self, index):
        self.widgets.indexSlider.setValue(index)

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
        raise NotImplementedError

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

    def calculateMPR(self):
        self.view.calculateMPR()

    def saveLengths(self):
        logger.info("Saving lengths to file...")
        # first argument of qfiledialog needs to be the qwidget itself
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Length Points As", config_data.get_config_value("DefaultSaveToFolder"),
                "%s Files (*.%s)" % ("json".upper(), "json"))

        if fileName:
            self.view.saveLengths(fileName)
            logger.info(f"Saved as {fileName}")

    def saveMPRPoints(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save MPR Points As", config_data.get_config_value("DefaultSaveToFolder"),
                "%s Files (*.%s);;All Files (*)" % ("json".upper(), "json"))

        if fileName:
            self.view.saveMPRPoints(fileName)

    def loadMPRPoints(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Load MPR points")

        if fileName:
            self.view.loadMPRPoints(fileName)

    def disablePointPicker(self):
        self.interactorStyle.actions["PickingMPR"] = 0
        self.interactorStyle.actions["PickingLength"] = 0

    def drawLengthLines(self):
        self.view.drawLengthLines()

    def drawMPRSpline(self):
        self.view.drawMPRSpline()
