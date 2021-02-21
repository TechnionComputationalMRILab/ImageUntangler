import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QComboBox, QSizePolicy

from Interfaces import SequenceViewerInterface


class SequenceInteractorWidgets:
    def __init__(self, MRIimages: List[str], parent: SequenceViewerInterface):
        self.manager = parent
        self.sequenceList = self.addSequenceList(MRIimages, parent)
        self.indexSlider = QSlider(Qt.Horizontal, parent=parent)
        self.windowSlider = QSlider(Qt.Horizontal, parent=parent)
        self.levelSlider = QSlider(Qt.Horizontal, parent=parent)
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
            basename = basename[:basename.rfind(".")]
            sequenceList.addItem(basename)

    def addSequenceList(self, MRIimages, parent) -> QComboBox:
        sequenceList = QComboBox(parent=parent)
        sequenceList.setSizePolicy(self._buildSizePolicy(sequenceList))
        self.addImages(sequenceList, MRIimages)
        return sequenceList

    def addActions(self):
        self.indexSlider.sliderMoved.connect(self.manager.changeIndex)
        self.windowSlider.sliderMoved.connect(self.manager.changeWindow)
        self.levelSlider.sliderMoved.connect(self.manager.changeLevel)
        self.sequenceList.currentIndexChanged.connect(self.manager.changeSequence)

    def setValues(self, sliceIdx: int, maxSlice: int, windowValue: int, levelValue: int) -> None:
        self.indexSlider.setMinimum(0) # not sure why order matters here, but setValue() must be last
        self.indexSlider.setMaximum(maxSlice)
        self.indexSlider.setValue(sliceIdx)
        self.windowSlider.setMaximum(int(2.5 * windowValue))
        self.windowSlider.setMinimum(windowValue - 800)
        self.windowSlider.setValue(windowValue)
        self.levelSlider.setMinimum(levelValue - 500)
        self.levelSlider.setMaximum(int(levelValue*2.5))
        self.levelSlider.setValue(levelValue)