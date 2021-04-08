from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List

from View.DICOMSliceViewer import DICOMSliceViewer
from Model.DICOMSequence import DICOMSequence
from Model.BaseViewerManager import BaseViewerManager
from MainWindowComponents.MessageBoxes import noGoodFiles, gzipFileMessage


class DICOMViewerManager(BaseViewerManager):
    def __init__(self, model, MRIimages: List[str]):
        super().__init__(model)
        self.sequences = DICOMSequence.get_dicom_seqs(MRIimages)
        self.current_sequence: DICOMSequence = self.sequences[0]

    def showValidImage(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        if self.goodIndex == -1: # first image is being loaded
            if sequenceIndex == len(self.sequences)-1:
                noGoodFiles()
            else:
                return self.loadSequence(sequenceIndex+1, VTKinteractor, interactorStyle)
        else:
            gzipFileMessage()
            return self.loadSequence(self.goodIndex, VTKinteractor, interactorStyle)

    def loadSequence(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        try:
            current_sequence = self.sequences[sequenceIndex]
            sequenceViewer = DICOMSliceViewer(self, VTKinteractor, interactorStyle, current_sequence.get_middle_slice(), current_sequence.get_index())
            _ = sequenceViewer.sliceIdx # test if image was loaded properly
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer
        except AttributeError:
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)

    def load_index(self, sliceIdx: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        self.goodIndex = sliceIdx
        return DICOMSliceViewer(self, VTKinteractor, interactorStyle,
                                self.sequences[self.goodIndex].get_slice(sliceIdx), sliceIdx)
