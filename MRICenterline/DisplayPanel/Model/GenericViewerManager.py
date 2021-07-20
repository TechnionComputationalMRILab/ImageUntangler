from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List
import os
# from icecream import ic

from MRICenterline.DisplayPanel.View.GenericSequenceViewer import GenericSequenceViewer
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class GenericViewerManager:
    def __init__(self, model, MRIimages):
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
            logging.debug(f"Loading {self.MRIimages.get_sequences()[sequenceIndex]}")

            sequenceViewer = GenericSequenceViewer(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex])
            _ = sequenceViewer.sliceIdx # test if image was loaded properly

            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer
        except AttributeError as err:
            logging.error(f"AttributeError found: {err}")
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)
        except FileNotFoundError as err:
            logging.error(f"FileNotFoundError found: {err}")
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)
                # logging.error(f"File not found: {self.MRIimages[sequenceIndex]}")
        except Exception as err:
            logging.critical(f"Error in loading sequence. Error is {err}")
