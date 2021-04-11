from typing import List, Tuple
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QMainWindow

from MPRwindow.MPRWindow import Ui_MPRWindow

from util import stylesheets
from View.Toolbar import Toolbar
from Model.getMPR import PointsToPlaneVectors


class BaseModel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.toolbar = Toolbar(parent=self, manager=self)
        self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        #self.interactor = QVTKRenderWindowInteractor(frame)
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False

#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

#_____________________________________________Interface to Widgets______________________________________________________________

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
        self.interactorStyle.actions["PickingMPR"] = int(not self.interactorStyle.actions["PickingMPR"])

    def reverseLengthPointsStatus(self):
        self.interactorStyle.actions["PickingLength"] = int(not self.interactorStyle.actions["PickingLength"])

    def calculateLengths(self):
        pass

    def calculateMPR(self):
        MPRproperties = PointsToPlaneVectors(self.view.MPRpoints.getCoordinatesArray(), self.view.imageData, Plot=0, height=40, viewAngle=180)
        MPR_M = MPRproperties.MPR_M
        delta = MPRproperties.delta
        MPRposition = MPRproperties.MPR_indexs_np
        self.openMPRWindow(MPR_M, delta, MPRposition, self.view.MPRpoints.getCoordinatesArray())

    def openMPRWindow(self, MPR_M, delta, MPRposition, points):
        window = QMainWindow()
        ui = Ui_MPRWindow()
        ui.setupUi(window, MPR_M, delta, MPRposition, points)
        window.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        window.show()