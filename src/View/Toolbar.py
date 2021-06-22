from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
# from icecream import ic


class Toolbar(QToolBar):
    def __init__(self, parent, manager):
        super().__init__(parent=parent)
        self.manager = manager
        self.addLengthMenu()
        self.addMPRMenu()
        self.addDisablePointPickers()
        self.showPickerStatus()

    def addLengthPointsAction(self):
        lengthPointAction = QAction("Add Length Points", self)
        lengthPointAction.setStatusTip("Set Length Points")
        lengthPointAction.triggered.connect(self.manager.disablePointPicker)
        lengthPointAction.triggered.connect(self.manager.reverseLengthPointsStatus)
        lengthPointAction.triggered.connect(lambda: self.changePickerStatus("length"))
        # self.addAction(lengthPointAction)
        return lengthPointAction

    def addLengthCalculation(self):
        lengthCalculation = QAction("Calculate Length", self)
        lengthCalculation.setStatusTip("Calculate length from available points")
        # lengthCalculation.triggered.connect(self.manager.drawLengthLines)
        lengthCalculation.triggered.connect(self.manager.calculateLengths)
        # self.addAction(lengthCalculation)
        return lengthCalculation

    def addLengthSave(self):
        lengthSave = QAction("Save Length", self)
        lengthSave.setStatusTip("Save the length as a file")
        lengthSave.triggered.connect(self.manager.saveLengths)
        return lengthSave

    def addLengthMenu(self):
        LengthPushButton = QPushButton("Length")
        menu = QMenu()
        menu.addAction(self.addLengthPointsAction())
        menu.addAction(self.addLengthCalculation())
        menu.addAction(self.addLengthSave())
        menu.addAction(self.loadLength())

        LengthPushButton.setMenu(menu)
        self.addWidget(LengthPushButton)

    def addMPRpointsAction(self):
        MPRpointsAction = QAction("Add MPR Points", self)
        MPRpointsAction.setStatusTip("Set MPR Points")
        MPRpointsAction.triggered.connect(self.manager.disablePointPicker)
        MPRpointsAction.triggered.connect(self.manager.reverseMPRpointsStatus)
        MPRpointsAction.triggered.connect(lambda: self.changePickerStatus("MPR"))
        # self.addAction(MPRpointsAction)
        return MPRpointsAction

    def addMPRcalculation(self):
        MPRcalculation = QAction("Calculate MPR", self)
        MPRcalculation.setStatusTip("Calculate MPR from available points")
        # MPRcalculation.triggered.connect(self.manager.drawMPRSpline)
        MPRcalculation.triggered.connect(self.manager.calculateMPR)
        # self.addAction(MPRcalculation)
        return MPRcalculation

    def addMPRSave(self):
        MPRSave = QAction("Save MPR Points", self)
        MPRSave.setStatusTip("Save the MPR points as a file")
        MPRSave.triggered.connect(self.manager.saveMPRPoints)
        return MPRSave

    def loadMPR(self):
        MPRLoad = QAction("Load MPR Points from file", self)
        MPRLoad.setStatusTip("Load the MPR points from file")
        MPRLoad.triggered.connect(self.manager.loadMPRPoints)
        # MPRLoad.triggered.connect(self.manager.calculateMPR)
        return MPRLoad

    def loadLength(self):
        LengthLoad = QAction("Load length points from file", self)
        LengthLoad.setStatusTip("Load length points from file")
        LengthLoad.triggered.connect(self.manager.loadLengthPoints)
        return LengthLoad

    def showMPRPanel(self):
        # for testing puposes
        LengthLoad = QAction("TEST", self)
        LengthLoad.setStatusTip("TESTING")
        LengthLoad.triggered.connect(self.manager.showMPRPanel)
        return LengthLoad

    def editAnnotation(self):
        # for testing puposes
        LengthLoad = QAction("TEST2", self)
        LengthLoad.setStatusTip("TESTING2")
        LengthLoad.triggered.connect(self.manager.modifyAnnotation)
        return LengthLoad


    def addMPRMenu(self):
        MPRPushButton = QPushButton("MPR Calculate")
        menu = QMenu()
        menu.addAction(self.addMPRpointsAction())
        menu.addAction(self.addMPRcalculation())
        menu.addAction(self.addMPRSave())
        menu.addAction(self.loadMPR())
        menu.addAction(self.showMPRPanel())
        menu.addAction(self.editAnnotation())

        MPRPushButton.setMenu(menu)
        self.addWidget(MPRPushButton)

    def showPickerStatus(self):
        self.PickerStatus = QLabel("EMPTY")
        font = QFont()
        font.setBold(True)
        self.PickerStatus.setFont(font)
        self.PickerStatus.clear()
        self.addWidget(self.PickerStatus)

    def addDisablePointPickers(self):
        DisablePPButton = QAction("Disable Point Picker", self)
        DisablePPButton.triggered.connect(self.manager.disablePointPicker)
        DisablePPButton.triggered.connect(lambda: self.PickerStatus.clear())

        self.addAction(DisablePPButton)

    def changePickerStatus(self, status):
        self.PickerStatus.setText(f"Picking {status} Points")
