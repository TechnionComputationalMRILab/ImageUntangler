from typing import List, Tuple
from icecream import ic
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QMainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MPRwindow.MPRWindow import Ui_MPRWindow

from util import stylesheets
from View.SlidersLayout import SlidersLayout
from View.Toolbar import Toolbar
from Model.ViewerManager import ViewerManager
from Model.getMPR import PointsToPlaneVectors
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MPRWindow2.MPRWindow import MPRWindow


class SequenceViewerInterface(QWidget):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        self.layout = QVBoxLayout(self)
        frame = self.buildFrame()
        self.toolbar = Toolbar(parent=self, manager=self)
        self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, interface=self)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.model = ViewerManager(self,  MRIimages)
        self.view = self.model.loadSequence(0, self.interactor, self.interactorStyle)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider,
                                      levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False

#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

    def initializeSliderValues(self):
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

#_____________________________________________Interface to Widgets______________________________________________________________

    def changeSequence(self, sequenceIndex: int):
        self.view = self.model.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

    def setListWidgetIndex(self, index):
        # sets index of sequences in list in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.view.adjustWindow(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.view.adjustLevel(level)

    def setIndex(self, index: int):
        self.view.setSliceIndex(index)

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
        self.view.adjustSliceIdx(changeFactor)
        self.widgets.indexSlider.setValue(self.view.sliceIdx)

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
        ic(self.view.MPRpoints)
        ic(len(self.view.MPRpoints))
        MPRproperties = PointsToPlaneVectors(self.view.MPRpoints.getCoordinatesArray(), self.view.imageData, Plot=0, height=40, viewAngle=180)

        MPR_M = MPRproperties.MPR_M
        delta = MPRproperties.delta
        MPRposition = MPRproperties.MPR_indexs_np
        self.openMPRWindow(MPR_M, delta, MPRposition, self.view.MPRpoints.getCoordinatesArray())

    def openMPRWindow(self, MPR_M, delta, MPRposition, points):
        # window = QMainWindow()
        MPRWindow(MPR_M, delta, MPRposition, points)
        # ui.show()