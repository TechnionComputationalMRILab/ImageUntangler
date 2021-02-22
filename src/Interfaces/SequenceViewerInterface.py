from typing import List
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget

from vtk import vtkMatrix4x4

from View.SlidersLayout import SlidersLayout
from Model.ViewerManager import ViewerManager
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from Control.AxialViewerInteractorStyle import AxialViewerInteractorStyle


class SequenceViewerInterface(QWidget):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        self.layout = QVBoxLayout(self)
        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = AxialViewerInteractorStyle(parent=self.interactor, interface=self)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.model = ViewerManager(self,  MRIimages)
        self.view = self.model.loadSequence(0, self.interactor, self.interactorStyle)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider, levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)

    def initializeSliderValues(self):
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

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


    #__________________________________________ InteractorStyle interface to view ________________________________

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


    def moveBullsEye(self, mouseCoordinates):
        self.interface.moveBullsEye(mouseCoordinates)

    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame