from PyQt5.QtWidgets import QFormLayout, QSlider, QLabel, QComboBox


class SlidersLayout(QFormLayout):
    def __init__(self, sequenceList: QComboBox, windowSlider: QSlider, levelSlider: QSlider, indexSlider: QSlider):
        super().__init__()
        self.setWidget(0, QFormLayout.FieldRole, sequenceList)
        self.addIndexSlider(indexSlider)
        self.addWindowSlider(windowSlider)
        self.addLevelSlider(levelSlider)

    def addCaption(self, captionText: str, row: int):
        caption = QLabel()
        caption.setText(captionText)
        self.setWidget(row, QFormLayout.LabelRole, caption)

    def addIndexSlider(self, indexSlider):
        self.setWidget(1, QFormLayout.FieldRole, indexSlider)
        self.addCaption("Slice Index", 1)

    def addLevelSlider(self, levelSlider):
        self.setWidget(2, QFormLayout.FieldRole, levelSlider)
        self.addCaption("Level", 2)

    def addWindowSlider(self, windowSlider):
        self.setWidget(3, QFormLayout.FieldRole, windowSlider)
        self.addCaption("Window", 3)
