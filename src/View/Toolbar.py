from PyQt5.QtWidgets import QToolBar, QAction


class Toolbar(QToolBar):
    def __init__(self, parent, manager):
        super().__init__(parent=parent)
        self.manager = manager
        self.addLengthPointsAction()
        self.addLengthCalculation()
        self.addMPRpointsAction()
        self.addMPRcalculation()

    def addLengthPointsAction(self):
        lengthPointAction = QAction("Add Length Points", self)
        lengthPointAction.setStatusTip("Set Length Points")
        lengthPointAction.triggered.connect(self.manager.reverseLengthPointsStatus)
        self.addAction(lengthPointAction)

    def addLengthCalculation(self):
        lengthCalculation = QAction("Calculate Length", self)
        lengthCalculation.setStatusTip("Calculate length from available points")
        lengthCalculation.triggered.connect(self.manager.calculateLengths)
        self.addAction(lengthCalculation)

    def addMPRpointsAction(self):
        MPRpointsAction = QAction("Add MPR Points", self)
        MPRpointsAction.setStatusTip("Set MPR Points")
        MPRpointsAction.triggered.connect(self.manager.reverseMPRpointsStatus)
        self.addAction(MPRpointsAction)

    def addMPRcalculation(self):
        MPRcalculation = QAction("Calculate MPR", self)
        MPRcalculation.setStatusTip("Calculate MPR from available points")
        MPRcalculation.triggered.connect(self.manager.calculateMPR)
        self.addAction(MPRcalculation)
