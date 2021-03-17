from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *


class MPRW_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        _layout = QVBoxLayout(self)

        _test_label = QLabel("top box goes here")

        _layout.addWidget(_test_label)

        # TODO: check if this is needed...
        # _menubar = QToolBar()
        # _menubar.setGeometry(QRect(0, 0, 990, 22))
        # _layout.addWidget(_menubar)
        #
        # _statusbar = QStatusBar()
        # _layout.addWidget(_statusbar)

        self._bottom_layout = QHBoxLayout()
        _layout.addLayout(self._bottom_layout)

        self.set_height_angle()
        self.buildLengthCalcBox()

        self._bottom_layout.addWidget(QLabel("2 bottom box here"))

        self.setLayout(_layout)

    def set_height_angle(self):
        _size_set_groupbox = QGroupBox(self)

        self.settingsBoxLayout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        self.settingsBoxLayout.addWidget(_height_label, Qt.AlignHCenter)
        self.heightSetter = QDoubleSpinBox(_size_set_groupbox)
        self.heightSetter.setMaximum(5000.0)
        self.heightSetter.setProperty("value", 20.0)
        self.heightSetter.setSuffix(" mm")
        self.settingsBoxLayout.addWidget(self.heightSetter, Qt.AlignHCenter)

        # angle
        _angle_label = QLabel("Angle")
        self.settingsBoxLayout.addWidget(_angle_label, Qt.AlignHCenter)
        self.angleSetter = QSpinBox(_size_set_groupbox)
        self.angleSetter.setSuffix(" °")
        self.angleSetter.setMaximum(180)
        self.settingsBoxLayout.addWidget(self.angleSetter, Qt.AlignHCenter)

        # update button
        self.updateButton = QPushButton(_size_set_groupbox)
        self.settingsBoxLayout.addWidget(self.updateButton, Qt.AlignHCenter)

        self._bottom_layout.addWidget(_size_set_groupbox)

    def buildLengthCalcBox(self):

        # self.lengthCalcBox = QGroupBox(self)
        # self.lengthCalcBox.setSizePolicy(self._buildCommonSizePolicy(self.lengthCalcBox.sizePolicy().hasHeightForWidth()))
        # self.lengthCalcBox.setObjectName("lengthCalcBox")

        self.verticalLayout = QVBoxLayout(self)

        self.setPointsButton = QPushButton("Set Points")
        self.verticalLayout.addWidget(self.setPointsButton, 0, Qt.AlignHCenter)
        self.calcLengthButton = QPushButton("Calculate Length")
        self.verticalLayout.addWidget(self.calcLengthButton, 0, Qt.AlignHCenter)
        self.saveButton = QPushButton("Save")
        self.verticalLayout.addWidget(self.saveButton, 0, Qt.AlignHCenter)
        self._bottom_layout.addWidget(self.verticalLayout)
