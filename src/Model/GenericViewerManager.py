from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List
import os

from View.GenericSequenceViewer import GenericSequenceViewer
from MainWindowComponents.MessageBoxes import noGoodFiles, gzipFileMessage

from util import logger
logger = logger.get_logger()


class GenericViewerManager:
    def __init__(self, model, MRIimages: List[str]):
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
        logger.debug(f"showValidImage function run. sequenceIndex: {sequenceIndex}")
        if self.goodIndex == -1: # first image is being loaded
            if sequenceIndex == len(self.MRIimages)-1:
                noGoodFiles()
            else:
                return self.loadSequence(sequenceIndex+1, VTKinteractor, interactorStyle)
        else:
            gzipFileMessage()
            return self.loadSequence(self.goodIndex, VTKinteractor, interactorStyle)

    def loadSequence(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        try:
            logger.debug(f"Loading {self.MRIimages[sequenceIndex]}")
            # sequenceViewer = NRRDSequenceViewer(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex],
            #                                     self.MRIimages[0][-4:] != "nrrd")
            sequenceViewer = GenericSequenceViewer(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex],
                                                self.MRIimages[sequenceIndex][-4:] != "nrrd")
            _ = sequenceViewer.sliceIdx # test if image was loaded properly
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer
        except AttributeError as err:
            logger.error(f"AttributeError found: {err}")
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)
        except FileNotFoundError as err:
            logger.error(f"FileNotFoundError found: {err}")
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)
                # logger.error(f"File not found: {self.MRIimages[sequenceIndex]}")
        except Exception as err:
            logger.critical(f"Error in loading sequence. Error is {err}")

