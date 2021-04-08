from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List

from View.NRRDSequenceViewer import NRRDSequenceViewer
from Model.BaseViewerManager import BaseViewerManager
from MainWindowComponents.MessageBoxes import noGoodFiles, gzipFileMessage


class NRRDViewerManager(BaseViewerManager):
    def __init__(self, model, MRIimages: List[str]):
        super().__init__(model)
        self.MRIimages = MRIimages

    def showValidImage(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
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
            sequenceViewer = NRRDSequenceViewer(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex],
                                                self.MRIimages[0][-4:] != "nrrd")
            _ = sequenceViewer.sliceIdx # test if image was loaded properly
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer
        except AttributeError:
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)

