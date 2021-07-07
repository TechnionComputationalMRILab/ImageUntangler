from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from View.SlidersLayout import SlidersLayout
from Model.BaseModel import BaseModel
from Model.NRRDViewerManager import NRRDViewerManager
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle

from util import logger
logger = logger.get_logger()


class NRRDViewerModel(BaseModel):
    def __init__(self, MRIimages: List[str]):
        super().__init__()
        frame = self.buildFrame()
        self.interactor = QVTKRenderWindowInteractor(frame)
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.sequenceManager = NRRDViewerManager(self, MRIimages)
        self.view = self.sequenceManager.loadSequence(0, self.interactor, self.interactorStyle)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider,
                                      levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)


#_________________________________________Constructor functions_____________________________________

    def initializeSliderValues(self):
        logger.info(f"Index value {int(self.view.sliceIdx)}")
        self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))

#_____________________________________________Interface to Widgets______________________________________________________________

    def changeSequence(self, sequenceIndex: int):
        logger.info(f"Sequence changed {sequenceIndex}")
        try:
            self.view = self.sequenceManager.loadSequence(sequenceIndex, self.interactor, self.interactorStyle)
            self.widgets.setValues(sliceIdx=int(self.view.sliceIdx), maxSlice = self.view.imageData.extent[5], windowValue=int(self.view.WindowVal), levelValue=int(self.view.LevelVal))
        except Exception as err:
            logger.critical(f"Error: {err}")

    def setIndex(self, index: int):
        logger.info(f"Set index {int(index)}")
        self.view.setSliceIndex(index)
#__________________________________________Interface to interactor style_____________________________________________

    def changeSliceIndex(self, changeFactor: int):
        self.view.adjustSliceIdx(changeFactor)
        self.widgets.indexSlider.setValue(self.view.sliceIdx)
