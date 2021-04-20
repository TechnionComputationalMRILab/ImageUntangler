class BaseViewerManager:
    def __init__(self, model):
        self.goodIndex = -1 # index of image that is properly encoded
        self.manager = model

    def loadSequence(self, n: int, interactor, interactorStyle):
        raise NotImplementedError

    def showValidImage(self, sequenceIndex: int, VTKinteractor, interactorStyle):
        raise NotImplementedError

    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)

    def updateSliderIndex(self, index):
        self.manager.updateSliderIndex(index)
