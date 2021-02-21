from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget

from View.SlidersLayout import SlidersLayout
from Model.ViewerManager import ViewerManager
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from typing import List


class SequenceViewerInterface(QWidget):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        self.layout = QVBoxLayout(self)
        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.model = ViewerManager(self,  MRIimages, self.interactor, self.widgets.indexSlider.value())
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider, levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)

    def initializeSliderValues(self):
        self.widgets.setValues(sliceIdx=int(self.model.sequenceViewer.sliceIdx), windowValue=int(self.model.sequenceViewer.WindowVal), levelValue=int(self.model.sequenceViewer.LevelVal))

    def changeSequence(self, sequenceIndex: int):
        pass

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.model.sequenceViewer.adjustWindow(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.model.sequenceViewer.adjustLevel(level)

    def changeIndex(self, index: int):
        pass

    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame