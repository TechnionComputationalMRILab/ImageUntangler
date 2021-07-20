import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qtawesome as qta

from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class DisplayPanelToolbar(QToolBar):
    def __init__(self, parent, manager):
        super().__init__(parent=parent)
        self.set_toolbar_display_style()

        self.manager = manager
        self.addInfoButton()
        self.addLengthMenu()
        self.addMPRMenu()
        self.addDisablePointPickers()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        self.showPickerStatus()

    def set_toolbar_display_style(self):
        if CFG.get_config_data('display', 'toolbar-style') == 'icon':
            pass
        elif CFG.get_config_data('display', 'toolbar-style') == 'text':
            pass
        else:
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def addInfoButton(self):
        _info_button = QPushButton("Info")
        _info_button.setStatusTip("TESTING")
        _info_button.setIcon(qta.icon('fa.info-circle'))
        _info_button.clicked.connect(self.manager.showPatientInfoTable)
        self.addWidget(_info_button)

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
        # lengthCalculation.triggered.connect(self.manager.drawLengthLines) # TODO
        lengthCalculation.triggered.connect(self.manager.calculateLengths)
        return lengthCalculation

    def addLengthSave(self):
        lengthSave = QAction("Save Length", self)
        lengthSave.setStatusTip("Save the length as a file")
        lengthSave.triggered.connect(self.manager.saveLengths)
        return lengthSave

    def addLengthMenu(self):
        LengthPushButton = QPushButton("Length")
        menu = QMenu()
        LengthPushButton.setIcon(qta.icon('fa5s.ruler'))
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
        MPRcalculation.triggered.connect(self.manager.showCenterlinePanel)
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

    def editAnnotation(self):
        LengthLoad = QAction("Edit annotation", self)
        LengthLoad.setStatusTip("TESTING: Edit annotation")
        LengthLoad.triggered.connect(self.manager.modifyAnnotation)
        return LengthLoad

    def addMPRMenu(self):
        MPRPushButton = QPushButton("MPR Calculate")
        MPRPushButton.setIcon(qta.icon('mdi.image-filter-center-focus-strong'))

        menu = QMenu()
        menu.addAction(self.addMPRpointsAction())
        menu.addAction(self.addMPRcalculation())
        menu.addAction(self.addMPRSave())
        menu.addAction(self.loadMPR())

        if CFG.get_testing_status('point-editing'):
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
        _disable_picker_button = QPushButton("Disable point picking")
        _disable_picker_button.setStatusTip("Disables active point picker")
        _disable_picker_button.setIcon(qta.icon('fa5.hand-point-up', 'fa5s.ban',
                              options=[{'scale_factor': 0.5,
                                        'active': 'fa5.hand-rock'},
                                       {'color': 'red'}]))
        _disable_picker_button.clicked.connect(self.manager.disablePointPicker)
        _disable_picker_button.clicked.connect(lambda: self.PickerStatus.setText(" "))
        self.addWidget(_disable_picker_button)

    def changePickerStatus(self, status):
        self.PickerStatus.setText(f"Picking {status} Points")
