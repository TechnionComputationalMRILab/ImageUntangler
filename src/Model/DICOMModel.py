from typing import List
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from View.SlidersLayout import SlidersLayout
from Model.BaseModel import BaseModel
from Model.DICOMViewerManager import DICOMViewerManager
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle

from util import logger
logger = logger.get_logger()


class DICOMViewerModel(BaseModel):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        # self.widgets = SequenceInteractorWidgets(MRIimages, self)  # ???
        self.sequenceManager = DICOMViewerManager(self, MRIimages)
        self.view = self.sequenceManager.loadSequence(0, self.interactor, self.interactorStyle)
        self.widgets = SequenceInteractorWidgets([str(sequence) for sequence in self.sequenceManager.sequences], self)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider,
                                      levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)


#_________________________________________Constructor functions_____________________________________

    def initializeSliderValues(self):
        current_sequence = self.sequenceManager.current_sequence
        self.widgets.setValues(sliceIdx=int(current_sequence.get_index()), maxSlice=current_sequence.max_index(), windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

#_____________________________________________Interface to Widgets_______________________________(_______________________________

    def changeSequence(self, sequenceIndex: int):
        self.view = self.sequenceManager.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
        current_sequence = self.sequenceManager.current_sequence
        self.widgets.setValues(sliceIdx=int(current_sequence.get_index()), maxSlice=current_sequence.max_index(), windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

    def setIndex(self, index: int):
        self.view = self.sequenceManager.loadIndex(index, self.interactor, self.interactorStyle)
        self.widgets.resetSliders(self.view.WindowVal, self.view.LevelVal)

#______________________________________________Interface to interactor style________________________________________________________

    def changeSliceIndex(self, changeFactor: int):
        """
        :param changeFactor: increment or decrement sequence
        """
        if changeFactor == -1:
            self.view = self.sequenceManager.decrementIndex(self.interactor, self.interactorStyle)
        elif changeFactor == 1:
            self.view = self.sequenceManager.incrementIndex(self.interactor, self.interactorStyle)
        self.widgets.indexSlider.setValue(self.view.sliceIdx)

