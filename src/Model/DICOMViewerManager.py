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
        self.current_viewer: DICOMSliceViewer = None

    def showValidImage(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        if self.goodIndex == -1: # first image is being loaded
            if sequenceIndex == len(self.sequences)-1:
                noGoodFiles()
            else:
                return self.loadSequence(sequenceIndex+1, VTKinteractor, interactorStyle)
        else:
            gzipFileMessage()
            return self.loadSequence(self.goodIndex, VTKinteractor, interactorStyle)

    def loadSequence(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle) -> DICOMSliceViewer:
        try:
            current_sequence = self.sequences[sequenceIndex]
            slice_viewer = DICOMSliceViewer(self, VTKinteractor, interactorStyle, current_sequence.get_middle_slice(), current_sequence.get_index())
            _ = slice_viewer.sliceIdx # test if image was loaded properly
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            self.current_viewer = slice_viewer
            return slice_viewer
        except AttributeError:
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)

    def incrementIndex(self, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle) -> DICOMSliceViewer:
        if self.goodIndex != len(self.current_sequence)-1:
            return self.loadIndex(self.goodIndex + 1, VTKinteractor, interactorStyle)
        else:
            return self.current_viewer

    def decrementIndex(self, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        if self.goodIndex != 0:
            return self.loadIndex(self.goodIndex - 1, VTKinteractor, interactorStyle)
        else:
            return self.current_viewer

    def loadIndex(self, sliceIdx: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        self.goodIndex = sliceIdx
        return DICOMSliceViewer(self, VTKinteractor, interactorStyle,
                                self.sequences[self.goodIndex].get_slice(sliceIdx), sliceIdx)
