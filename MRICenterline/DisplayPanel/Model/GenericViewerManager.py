from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.DisplayPanel.View.GenericSequenceViewer import GenericSequenceViewer
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class GenericViewerManager:
    def __init__(self, model, MRIimages: Imager):
        self.MRIimages = MRIimages
        self.goodIndex = -1 # index of image that is properly encoded
        self.manager = model

    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)

    def updateSliderIndex(self, index):
        self.manager.updateSliderIndex(index)

    def showValidImage(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        logging.debug(f"showValidImage function run. sequenceIndex: {sequenceIndex}")
        if self.goodIndex == -1: # first image is being loaded
            if sequenceIndex == len(self.MRIimages)-1:
                logging.error("Bad files?")
                MSG.msg_box_warning("Bad files!")
            else:
                return self.loadSequence(sequenceIndex+1, VTKinteractor, interactorStyle)
        else:
            logging.error("gzip files?")
            MSG.msg_box_warning("GZip files, but you shouldnt be seeing this error")
            return self.loadSequence(self.goodIndex, VTKinteractor, interactorStyle)

    def loadSequence(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        try:
            logging.debug(f"Loading sequence {sequenceIndex} / {self.MRIimages.get_sequences()[sequenceIndex]}")

            sequenceViewer = GenericSequenceViewer(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex])
        except Exception as err:
            logging.critical(f"Error in loading sequence. Error is {err}")
        else:
            _ = sequenceViewer.sliceIdx

            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer

    def load_single_sequence(self, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle, single_image):
        logging.debug(f"Loading single sequence")
        return GenericSequenceViewer(self, VTKinteractor, interactorStyle, single_image)
