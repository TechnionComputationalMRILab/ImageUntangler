from View.MRISequenceViewer import PlaneViewerQT
from MainWindowComponents.MessageBoxes import gzipFileMessage, noGoodFiles
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List


class ViewerManager:
    def __init__(self, interface, MRIimages: List[str]):
        self.goodIndex = -1 # index of image that is properly encoded
        self.manager = interface
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
            sequenceViewer = PlaneViewerQT(self, VTKinteractor, interactorStyle, self.MRIimages[sequenceIndex],
                                                self.MRIimages[0][-4:] != "nrrd")
            _ = sequenceViewer.sliceIdx # test if image was loaded properly
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
            return sequenceViewer
        except AttributeError:
            return self.showValidImage(sequenceIndex, VTKinteractor, interactorStyle)

    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)

    def updateSliderIndex(self, index):
        self.manager.updateSliderIndex(index)