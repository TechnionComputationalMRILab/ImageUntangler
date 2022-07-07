from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
import qtawesome as qta

from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display import toolbar_connect


class DisplayPanelToolbarButtons(QWidget):
    def __init__(self,
                 model: CaseModel,
                 parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)

        column = 0

        save_button = QPushButton(qta.icon('fa.save'), "Save")
        save_button.setFlat(True)
        layout.addWidget(save_button, 0, column, 1, 1)
        save_button.clicked.connect(lambda: toolbar_connect.save(model))

        export_button = QPushButton(qta.icon("fa5s.file-export"), "Export")
        export_button.setFlat(True)
        layout.addWidget(export_button, 1, column, 1, 1)
        export_button.clicked.connect(lambda: toolbar_connect.export(model, parent))

        column += 1  # NEW COLUMN

        def enable_length_picking(s):
            if s:
                toolbar_connect.set_picker_status(model, PickerStatus.PICKING_LENGTH)

                winlev_button.setChecked(not s)
                mpr_button.setChecked(not s)
            else:
                toolbar_connect.set_picker_status(model, PickerStatus.NOT_PICKING)

        length_button = QPushButton(qta.icon('mdi.ruler'), "Length")
        length_button.setCheckable(True)
        length_button.setChecked(False)
        layout.addWidget(length_button, 0, column, 1, 1)
        length_button.clicked.connect(enable_length_picking)

        measure_length_button = QPushButton(qta.icon('mdi.tape-measure'), "Measure Length")
        measure_length_button.setFlat(True)
        measure_length_button.setEnabled(True)
        layout.addWidget(measure_length_button, 1, column, 1, 1)
        measure_length_button.clicked.connect(lambda: toolbar_connect.calculate(model, PointStatus.LENGTH))

        column += 1  # NEW COLUMN

        def enable_mpr_picking(s):
            if s:
                toolbar_connect.set_picker_status(model, PickerStatus.PICKING_MPR)
                winlev_button.setChecked(not s)
                length_button.setChecked(not s)
            else:
                toolbar_connect.set_picker_status(model, PickerStatus.NOT_PICKING)

        mpr_button = QPushButton(qta.icon('mdi.image-filter-center-focus-strong'), "MPR")
        mpr_button.setCheckable(True)
        layout.addWidget(mpr_button, 0, column, 1, 1)
        mpr_button.clicked.connect(enable_mpr_picking)

        calculate_mpr_button = QPushButton(qta.icon('mdi.calculator'), "Calculate MPR")
        calculate_mpr_button.setFlat(True)
        calculate_mpr_button.setEnabled(True)
        layout.addWidget(calculate_mpr_button, 1, column, 1, 1)
        calculate_mpr_button.clicked.connect(lambda: toolbar_connect.calculate(model, PointStatus.MPR))

        column += 1  # NEW COLUMN

        select_point_button = QPushButton(qta.icon("mdi.select-search"), "Select MPR point")
        layout.addWidget(select_point_button, 0, column, 1, 1)
        select_point_button.setFlat(True)
        select_point_button.clicked.connect(lambda: toolbar_connect.find_point(model))

        def show_hide_mpr_markers(s):
            toolbar_connect.toggle_mpr_marker(model, s)
            if s:
                mpr_markers_button.setText("Show MPR markers")
            else:
                mpr_markers_button.setText("Hide MPR markers")

        mpr_markers_button = QPushButton("Hide MPR markers")
        layout.addWidget(mpr_markers_button, 1, column, 1, 1)
        mpr_markers_button.setCheckable(True)
        mpr_markers_button.setChecked(False)
        mpr_markers_button.clicked.connect(show_hide_mpr_markers)

        column += 1  # NEW COLUMN

        undo_button = QPushButton(qta.icon('mdi.undo'), "Undo")
        undo_button.setFlat(True)
        layout.addWidget(undo_button, 0, column, 1, 1)
        undo_button.clicked.connect(lambda: toolbar_connect.undo(model))

        clear_all_button = QPushButton(qta.icon('mdi.restart'), "Clear All")
        clear_all_button.setFlat(True)
        layout.addWidget(clear_all_button, 1, column, 1, 1)
        clear_all_button.clicked.connect(lambda: toolbar_connect.undo(model, undo_all=True))

        column += 1  # NEW COLUMN

        patient_info_button = QPushButton(qta.icon('mdi.folder-information'), "Patient Info")
        patient_info_button.setFlat(True)
        layout.addWidget(patient_info_button, 0, column, 1, 1)
        patient_info_button.clicked.connect(lambda: toolbar_connect.patient_info(model, parent))

        comment_button = QPushButton(qta.icon('mdi.comment-edit'), "Add Comment")
        comment_button.setFlat(True)
        layout.addWidget(comment_button, 1, column, 1, 1)
        comment_button.clicked.connect(lambda: toolbar_connect.comment(model, parent))

        def reset_other_picker_buttons(s):
            toolbar_connect.set_picker_status(model, PickerStatus.NOT_PICKING)

            if s:
                length_button.setChecked(not s)
                mpr_button.setChecked(not s)

        column += 1  # NEW COLUMN

        winlev_button = QPushButton(qta.icon('mdi.lock-reset'), "Window/level")
        winlev_button.setCheckable(True)
        winlev_button.setChecked(True)
        layout.addWidget(winlev_button, 0, column, 1, 1)
        winlev_button.clicked.connect(reset_other_picker_buttons)

        def show_hide_intermediate_points(s):
            toolbar_connect.intermediate_points(model, s)
            if s:
                intermediate_points_button.setIcon(qta.icon('mdi.middleware'))
                intermediate_points_button.setText("Show intermediate points")
            else:
                intermediate_points_button.setIcon(qta.icon('mdi.middleware-outline'))
                intermediate_points_button.setText("Hide intermediate points")

        intermediate_points_button = QPushButton(qta.icon('mdi.middleware-outline'), "Hide intermediate points")
        intermediate_points_button.setCheckable(True)
        intermediate_points_button.setChecked(False)
        layout.addWidget(intermediate_points_button, 1, column, 1, 1)
        intermediate_points_button.clicked.connect(show_hide_intermediate_points)

        column += 1  # NEW COLUMN

        def timer_start(s):
            timer_pause.setEnabled(s)
            timer_pause.setText("Pause timer")
            timer_pause.setIcon(qta.icon("mdi.pause"))
            if s:
                toolbar_connect.timer_status(model, "START")
                timer_button.setIcon(qta.icon('mdi.timer-outline'))
                timer_button.setText("Stop timer")
            else:
                toolbar_connect.timer_status(model, "STOP")
                timer_button.setIcon(qta.icon('mdi.timer-off-outline'))
                timer_button.setText("Start Timer")

        def timer_pause_resume(s):
            if s:
                toolbar_connect.timer_status(model, "PAUSE")
                timer_pause.setIcon(qta.icon("mdi.play"))
                timer_pause.setText("Resume timer")
            else:
                toolbar_connect.timer_status(model, "RESUME")
                timer_pause.setIcon(qta.icon("mdi.pause"))
                timer_pause.setText("Pause timer")

        timer_button = QPushButton(qta.icon('mdi.timer-off-outline'), "Start Timer")
        timer_button.setCheckable(True)
        layout.addWidget(timer_button, 0, column, 1, 1)
        timer_button.clicked.connect(timer_start)

        timer_pause = QPushButton(qta.icon("mdi.pause"), "Timer not started")
        timer_pause.setCheckable(True)
        timer_pause.setChecked(False)
        timer_pause.setEnabled(False)
        layout.addWidget(timer_pause, 1, column, 1, 1)
        timer_pause.clicked.connect(timer_pause_resume)
