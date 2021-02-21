from View.MRISequenceViewer import PlaneViewerQT
from MainWindowComponents.MessageBoxes import gzipFileMessage, noGoodFiles
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List


class ViewerManager:
    def __init__(self, interface, MRIimages: List[str], VTKinteractor: QVTKRenderWindowInteractor):
        self.goodIndex = -1 # index of image that is properly encoded
        self.manager = interface
        self.MRIimages = MRIimages
        self.VTKinteractor = VTKinteractor
        self.loadSequence(0)

    def showValidImage(self, sequenceIndex: int):
        if self.goodIndex == -1: # first image is being loaded
            if sequenceIndex == len(self.MRIimages)-1:
                noGoodFiles()
            else:
                self.loadSequence(sequenceIndex+1)
        else:
            gzipFileMessage()
            self.loadSequence(self.goodIndex)

    def loadSequence(self, sequenceIndex: int):
        try:
            self.sequenceViewer = PlaneViewerQT(self, self.VTKinteractor, self.MRIimages[sequenceIndex],
                                                self.MRIimages[0][-4:] != "nrrd")
            _ = self.sequenceViewer.sliceIdx # test if image was loaded properly
            print(self.sequenceViewer.sliceIdx)
            self.goodIndex = sequenceIndex
            self.manager.setListWidgetIndex(self.goodIndex)
        except AttributeError:
            self.showValidImage(sequenceIndex)

    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)

    def updateSliderIndex(self, index):
        self.manager.updateSliderIndex(index)