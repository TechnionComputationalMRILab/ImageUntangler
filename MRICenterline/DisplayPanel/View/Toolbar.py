from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QToolBar, QSizePolicy, QPushButton, QMenu, QLabel, QHBoxLayout
from PyQt5.Qt import Qt, QAction
import qtawesome as qta

from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


class DisplayPanelToolbar(QToolBar):
    def __init__(self, parent, manager):
        super().__init__(parent=parent)
        self.set_toolbar_display_style()
        self.manager = manager

        self.set_up_toolbar_order()

    def set_up_toolbar_order(self):
        self.addSaveAnnotationButton()

        self.addLengthMenu()
        self.addMPRMenu()

        self.addSeparator()

        self.addDisablePointPickers()
        self.addUndoButton()
        self.addDeleteAllButton()

        self.resetSlidersToDefault()

        self.addSeparator()

        self.add_export_menu()

        self.addSeparator(expand=True)

        self.addHideIntermediatePointsButton()
        self.addInfoButton()
        self.addTimerButton()

    def addSeparator(self, expand=False):
        if expand:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.addWidget(spacer)

    def set_toolbar_display_style(self):
        if CFG.get_config_data('display', 'toolbar-style') == 'icon':
            pass
        elif CFG.get_config_data('display', 'toolbar-style') == 'text':
            pass
        else:
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def addSaveAnnotationButton(self):
        _save_button = QPushButton("Save all annotations")
        _save_button = QPushButton("Save all annotations")
        _save_button.setIcon(qta.icon('fa.save'))
        _save_button.clicked.connect(self.manager.save_all)
        self.addWidget(_save_button)

    def addInfoButton(self):
        _info_button = QPushButton("Patient Info / Add comment")
        _info_button.adjustSize()
        _info_button.setStatusTip("Show patient info from DICOM file")
        _info_button.setIcon(qta.icon('fa.info-circle'))
        _info_button.clicked.connect(self.manager.showPatientInfoTable)
        self.addWidget(_info_button)

    def addLengthPointsAction(self):
        lengthPointAction = QAction("Add Length Points", self)
        lengthPointAction.setStatusTip("Set Length Points")
        lengthPointAction.triggered.connect(self.manager.disablePointPicker)
        lengthPointAction.triggered.connect(self.manager.reverseLengthPointsStatus)
        return lengthPointAction

    def addLengthCalculation(self):
        lengthCalculation = QAction("Calculate Length", self)
        lengthCalculation.setStatusTip("Calculate length from available points")
        # lengthCalculation.triggered.connect(self.manager.drawLengthLines) # TODO
        lengthCalculation.triggered.connect(self.manager.calculateLengths)
        return lengthCalculation

    def addLengthMenu(self):
        LengthPushButton = QPushButton("Length")
        menu = QMenu()
        LengthPushButton.setIcon(qta.icon('fa5s.ruler'))
        menu.addAction(self.addLengthPointsAction())
        menu.addAction(self.addLengthCalculation())

        LengthPushButton.setMenu(menu)
        self.addWidget(LengthPushButton)

    def addMPRpointsAction(self):
        MPRpointsAction = QAction("Add MPR Points", self)
        MPRpointsAction.setStatusTip("Set MPR Points")
        MPRpointsAction.triggered.connect(self.manager.disablePointPicker)
        MPRpointsAction.triggered.connect(self.manager.reverseMPRpointsStatus)
        return MPRpointsAction

    def addMPRcalculation(self):
        MPRcalculation = QAction("Calculate MPR", self)
        MPRcalculation.setStatusTip("Calculate MPR from available points")
        MPRcalculation.triggered.connect(self.manager.showCenterlinePanel)
        return MPRcalculation

    def addMPRMenu(self):
        MPRPushButton = QPushButton("MPR Calculations")
        MPRPushButton.adjustSize()
        MPRPushButton.setIcon(qta.icon('mdi.image-filter-center-focus-strong'))

        menu = QMenu()
        menu.addAction(self.addMPRpointsAction())
        menu.addAction(self.addMPRcalculation())

        MPRPushButton.setMenu(menu)
        self.addWidget(MPRPushButton)

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

    def resetSlidersToDefault(self):
        pass

    def addUndoButton(self):
        _undo_button = QPushButton("Undo last point")
        _undo_button.setStatusTip("Removes last point added")
        _undo_button.setIcon(qta.icon('fa5s.undo-alt'))
        _undo_button.clicked.connect(self.manager.undoAnnotation)
        self.addWidget(_undo_button)

    def addTimerButton(self):
        def toggleTimer():
            if not _timer_button.isChecked():
                _timer_button.setIcon(qta.icon('mdi.timer-outline'))
                _timer_button.setText("Start timer")
                self.manager.stop_timer()
                _pause_timer_button.setEnabled(False)

                if _pause_timer_button.isChecked():
                    _pause_timer_button.setChecked(False)
                    _pause_timer_button.setIcon(qta.icon("ei.pause-alt"))
                    _pause_timer_button.setText("Pause timer")
                    self.manager.resume_timer()
            else:
                _timer_button.setIcon(qta.icon('mdi.timer-off-outline'))
                _timer_button.setText("Stop timer")
                self.manager.start_timer()
                _pause_timer_button.setEnabled(True)

        def togglePause():
            if not _pause_timer_button.isChecked():
                _pause_timer_button.setIcon(qta.icon("ei.pause-alt"))
                _pause_timer_button.setText("Pause timer")
                self.manager.resume_timer()
            else:
                _pause_timer_button.setIcon(qta.icon("ei.play-alt"))
                _pause_timer_button.setText('Resume timer')
                self.manager.pause_timer()

        _timer_widget = QWidget()
        _timer_layout = QHBoxLayout()
        _timer_widget.setLayout(_timer_layout)

        _timer_button = QPushButton("Start timer")
        _pause_timer_button = QPushButton("Pause timer")

        _timer_button.setStatusTip("Start timer")
        _timer_button.setIcon(qta.icon('mdi.timer-outline'))
        _timer_button.setCheckable(True)
        _timer_button.clicked.connect(toggleTimer)
        _timer_layout.addWidget(_timer_button)

        _pause_timer_button.setCheckable(True)
        _pause_timer_button.setEnabled(False)
        _pause_timer_button.clicked.connect(togglePause)
        _pause_timer_button.setIcon(qta.icon("ei.pause-alt"))
        _timer_layout.addWidget(_pause_timer_button)

        self.addWidget(_timer_widget)

    def addDeleteAllButton(self):
        _delete_all = QPushButton("Clear points")
        _delete_all.setIcon(qta.icon('mdi.delete-outline'))
        _delete_all.clicked.connect(self.manager.deleteAllPoints)
        self.addWidget(_delete_all)

    def addHideIntermediatePointsButton(self):
        self._intermediate_points_button = QPushButton("Hide Intermediate MPR points")
        self._intermediate_points_button.setStatusTip("Hide all MPR points")
        self._intermediate_points_button.setIcon(qta.icon('mdi.laser-pointer', 'fa5s.ban',
                                                          options=[{'scale_factor': 0.5,
                                                                    'active': 'mdi.laser-pointer'},
                                                                   {'color': 'red'}]))
        self._intermediate_points_button.setCheckable(True)
        self._intermediate_points_button.clicked.connect(self.toggleIntermediatePoints)

        self.addWidget(self._intermediate_points_button)

    def toggleIntermediatePoints(self):
        if not self._intermediate_points_button.isChecked():
            self._intermediate_points_button.setIcon(qta.icon('mdi.laser-pointer', 'fa5s.ban',
                                                          options=[{'scale_factor': 0.5,
                                                                    'active': 'mdi.laser-pointer'},
                                                                   {'color': 'red'}]))
            self._intermediate_points_button.setText("Hide Intermediate MPR points")
            self.manager.show_intermediate_points()

        else:
            self._intermediate_points_button.setIcon(qta.icon('mdi.laser-pointer'))
            self._intermediate_points_button.setText("Show Intermediate MPR points")
            self.manager.hide_intermediate_points()

    def add_export_menu(self):
        export_button = QPushButton("Export...")
        export_button.adjustSize()
        export_button.setIcon(qta.icon('fa5s.file-export'))

        export_one_action = QAction("Export single sequence", self)
        export_one_action.triggered.connect(self.manager.export_one_sequence)

        export_entire_case = QAction("Export all sequences in case", self)
        # export_entire_case.triggered.connect(self.manager.export_entire_case)

        export_sequence_and_points = QAction("Export sequence with points", self)
        export_sequence_and_points.triggered.connect(self.manager.export_seq_and_pts)

        menu = QMenu()
        menu.addAction(export_one_action)
        menu.addAction(export_one_action)
        menu.addAction(export_sequence_and_points)

        export_button.setMenu(menu)
        self.addWidget(export_button)
