import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QComboBox, QSizePolicy


class SequenceInteractorWidgets:
    def __init__(self, MRISequences, model):
        self.model = model
        self.sequenceList = self.addSequenceList(MRISequences, model)
        self.indexSlider = QSlider(Qt.Horizontal, parent=model)
        self.windowSlider = QSlider(Qt.Horizontal, parent=model)
        self.levelSlider = QSlider(Qt.Horizontal, parent=model)
        self.addActions()

    def _buildSizePolicy(self, sequenceListBox: QComboBox) -> QSizePolicy:
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sequenceListBox.sizePolicy().hasHeightForWidth())
        return sizePolicy

    def addImages(self, sequenceList, MRIimages):
        for i in range(len(MRIimages)):
            basename = os.path.basename(MRIimages[i])
            suffix_index = basename.rfind(".")
            if suffix_index != -1:
                basename = basename[:suffix_index]
            sequenceList.addItem(basename)

    def addSequenceList(self, MRIimages, parent) -> QComboBox:
        sequenceList = QComboBox(parent=parent)
        sequenceList.setSizePolicy(self._buildSizePolicy(sequenceList))
        self.addImages(sequenceList, MRIimages)
        return sequenceList

    def addActions(self):
        self.indexSlider.sliderMoved.connect(self.model.setIndex)
        self.windowSlider.sliderMoved.connect(self.model.changeWindow)
        self.levelSlider.sliderMoved.connect(self.model.changeLevel)
        self.sequenceList.currentIndexChanged.connect(self.model.changeSequence)

    def setValues(self, sliceIdx: int, maxSlice: int, windowValue: int, levelValue: int) -> None:
        self.indexSlider.setMinimum(0) # setValue() must be last
        self.indexSlider.setMaximum(maxSlice)
        self.indexSlider.setValue(sliceIdx)
        self.windowSlider.setMaximum(int(2.5 * windowValue))
        self.windowSlider.setMinimum(max(1, windowValue - 800))
        self.windowSlider.setValue(windowValue)
        self.levelSlider.setMinimum(max(levelValue - 400, 1))
        self.levelSlider.setMaximum(int(levelValue*2.5))
        self.levelSlider.setValue(levelValue)

    def resetSliders(self, windowValue: int, levelValue: int):
        self.windowSlider.setMaximum(int(2.5 * windowValue))
        self.windowSlider.setMinimum(max(windowValue - 900, 1))
        self.windowSlider.setValue(windowValue)
        self.levelSlider.setMinimum(max(levelValue - 500, 1))
        self.levelSlider.setMaximum(int(levelValue*2.5))
        self.levelSlider.setValue(levelValue)
