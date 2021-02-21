from MRISequenceViewer import PlaneViewerQT
from MainWindowComponents.MessageBoxes import gzipFileMessage, noGoodFiles
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List


class ViewerManager:
    def __init__(self, interface, MRIimages: List[str], VTKinteractor: QVTKRenderWindowInteractor, currentIndex: int):
        self.goodIndex = -1 # index of image that is properly encoded
        self.manager = interface
        self.MRIimages = MRIimages
        self.currentIndex = currentIndex
        self.VTKinteractor = VTKinteractor
        self.sequenceViewer = self.loadSequence()

    def showValidImage(self):
        if self.goodIndex == -1: # first image is being loaded
            if self.currentIndex == len(self.MRIimages)-1:
                noGoodFiles()
            else:
                self.currentIndex+=1
                self.loadSequence()
        else:
            self.currentIndex = self.goodIndex
            gzipFileMessage()
            self.loadSequence()

    def loadSequence(self):
        try:
            self.sequenceViewer = PlaneViewerQT(self, self.VTKinteractor, self.MRIimages[int(self.currentIndex)],
                                             self.MRIimages[0][-4:] != "nrrd")
            self.goodIndex = self.currentIndex
            return self.sequenceViewer
        except AttributeError:
            self.showValidImage()


    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)
