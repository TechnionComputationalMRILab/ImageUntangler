from typing import List
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget

from vtk import vtkMatrix4x4

from View.SlidersLayout import SlidersLayout
from Model.ViewerManager import ViewerManager
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets


class SequenceViewerInterface(QWidget):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        self.layout = QVBoxLayout(self)
        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.model = ViewerManager(self,  MRIimages, self.interactor)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider, levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)

    def initializeSliderValues(self):
        self.widgets.setValues(sliceIdx=int(self.model.sequenceViewer.sliceIdx), maxSlice = self.model.sequenceViewer.imageData.extent[5], windowValue=int(self.model.sequenceViewer.WindowVal), levelValue=int(self.model.sequenceViewer.LevelVal))

    def changeSequence(self, sequenceIndex: int):
        self.model.loadSequence(sequenceIndex)

    def setListWidgetIndex(self, index):
        # sets index of sequences in list in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.model.sequenceViewer.adjustWindow(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.model.sequenceViewer.adjustLevel(level)

    def changeIndex(self, index: int):
        matrix: vtkMatrix4x4 = self.model.sequenceViewer.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, self.model.sequenceViewer.reslice.GetOutput().GetSpacing()[2], 1))
        if 0 <= index <= self.model.sequenceViewer.imageData.extent[5]:
            self.model.sequenceViewer.UpdateViewerMatrixCenter(center, index)

    def updateSliderIndex(self, index):
        self.widgets.indexSlider.setValue(index)

    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame