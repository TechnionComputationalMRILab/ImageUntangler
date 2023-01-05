from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QWidget, QPlainTextEdit
import qtawesome as qta

from MRICenterline import CFG
from MRICenterline.gui.display.toolbar_connect import *
from MRICenterline.gui.window.AnimatedToggle import AnimatedToggle


class ControlPanel(QDialog):
    def __init__(self, parent=None, model=None):
        QDialog.__init__(self, parent)
        self.setModal(False)
        self.setWindowTitle("Controls")

        self.parent = parent
        self.model = model

        layout = QGridLayout(self)
        self.setLayout(layout)
        self.move(100, 150)

        layout.addWidget(self.top(), 0, 0, 1, 2)
        layout.addWidget(self.point_panel(), 1, 0, 1, 1)
        layout.addWidget(self.overlay_options_panel(), 1, 1, 1, 1)
        layout.addWidget(self.centerline(), 2, 0, 1, 2)

        if CFG.get_testing_status("disable-all-testing-features"):
            layout.addWidget(self.debug(), 3, 0, 1, 2)

    def attach_model(self, model):
        self.model = model

    def top(self) -> QWidget:
        frame = QWidget(self)
        layout = QGridLayout(frame)

        save_button = QPushButton(qta.icon('fa.save'), "Save")
        save_button.clicked.connect(lambda: save(self.model))
        layout.addWidget(save_button, 0, 0, 1, 1)

        calculate_mpr_button = QPushButton(qta.icon('mdi.calculator'), "Calculate MPR")
        # TODO: QoL: disable when no MPR points are available
        layout.addWidget(calculate_mpr_button, 0, 1, 1, 1)
        calculate_mpr_button.clicked.connect(lambda: calculate(self.model, PointStatus.MPR))

        timer_button = QPushButton(qta.icon('mdi.timer-off-outline'), "TEMPORARY TIMER")
        layout.addWidget(timer_button, 1, 0, 1, 2)

        return frame

    def point_panel(self) -> QWidget:
        frame = QWidget(self)
        layout = QGridLayout(frame)

        button_list = []

        def flip_checked_status(picker_status):
            for button, status in button_list:
                if status == picker_status:
                    pass
                else:
                    button.setChecked(False)

        layout.addWidget(QLabel("Points"), 0, 0, 1, 2)
        layout.addWidget(QLabel("Add points"), 1, 0, 1, 2)

        add_length_widget = AnimatedToggle("Length", checked_color=CFG.get_hex_color("length-display-style", "color"))
        layout.addWidget(add_length_widget, 2, 0, 1, 1)
        add_length_button = add_length_widget.button
        button_list.append((add_length_button, PickerStatus.PICKING_LENGTH))
        add_length_button.clicked.connect(lambda: flip_checked_status(PickerStatus.PICKING_LENGTH))
        add_length_button.clicked.connect(lambda: set_picker_status(self.model, PickerStatus.PICKING_LENGTH))

        add_mpr_widget = AnimatedToggle("MPR", checked_color=CFG.get_hex_color("mpr-display-style", "color"))
        layout.addWidget(add_mpr_widget, 2, 1, 1, 1)
        add_mpr_button = add_mpr_widget.button
        button_list.append((add_mpr_button, PickerStatus.PICKING_MPR))
        add_mpr_button.clicked.connect(lambda: flip_checked_status(PickerStatus.PICKING_MPR))
        add_mpr_button.clicked.connect(lambda: set_picker_status(self.model, PickerStatus.PICKING_MPR))

        layout.addWidget(QLabel("Highlight points"), 3, 0, 1, 2)

        select_length_widget = AnimatedToggle("Length", checked_color=CFG.get_hex_color("length-display-style", "color"))
        layout.addWidget(select_length_widget, 4, 0, 1, 1)
        select_length_button = select_length_widget.button
        button_list.append((select_length_button, PickerStatus.FIND_LENGTH))
        select_length_button.clicked.connect(lambda: flip_checked_status(PickerStatus.FIND_LENGTH))
        # select_length_button.clicked.connect(lambda: find_point(self.model, PickerStatus.FIND_LENGTH))
        # TODO: implement length picking

        select_mpr_widget = AnimatedToggle("MPR", checked_color=CFG.get_hex_color("mpr-display-style", "color"))
        layout.addWidget(select_mpr_widget, 4, 1, 1, 1)
        select_mpr_button = select_mpr_widget.button
        button_list.append((select_mpr_button, PickerStatus.FIND_MPR))
        select_mpr_button.clicked.connect(lambda: flip_checked_status(PickerStatus.FIND_MPR))
        select_mpr_button.clicked.connect(lambda: find_point(self.model, PickerStatus.FIND_MPR))

        layout.addWidget(QLabel("Edit points"), 5, 0, 1, 2)

        edit_length_widget = AnimatedToggle("Length", checked_color=CFG.get_hex_color("length-display-style", "color"))
        layout.addWidget(edit_length_widget, 6, 0, 1, 1)
        edit_length_button = edit_length_widget.button
        button_list.append((edit_length_button, PickerStatus.MODIFYING_LENGTH))
        edit_length_button.clicked.connect(lambda: flip_checked_status(PickerStatus.MODIFYING_LENGTH))
        # edit_length_button.clicked.connect(lambda: edit_points(self.model, PickerStatus.MODIFYING_LENGTH))
        # TODO: implement length modifying

        edit_mpr_widget = AnimatedToggle("MPR", checked_color=CFG.get_hex_color("mpr-display-style", "color"))
        layout.addWidget(edit_mpr_widget, 6, 1, 1, 1)
        edit_mpr_button = edit_mpr_widget.button
        button_list.append((edit_mpr_button, PickerStatus.MODIFYING_MPR))
        edit_mpr_button.clicked.connect(lambda: flip_checked_status(PickerStatus.MODIFYING_MPR))
        edit_mpr_button.clicked.connect(lambda: edit_points(self.model, PickerStatus.MODIFYING_MPR))

        undo_button = QPushButton(qta.icon('mdi.undo'), "Undo")
        layout.addWidget(undo_button, 7, 0, 1, 1)
        undo_button.clicked.connect(lambda: undo(self.model))

        clear_all_button = QPushButton(qta.icon('mdi.restart'), "Clear All")
        layout.addWidget(clear_all_button, 7, 1, 1, 1)
        clear_all_button.clicked.connect(lambda: undo(self.model, undo_all=True))

        adjust_contrast_button = QPushButton("Adjust contrast")
        layout.addWidget(adjust_contrast_button, 8, 0, 1, 2)
        adjust_contrast_button.clicked.connect(lambda: flip_checked_status(PickerStatus.NOT_PICKING))
        adjust_contrast_button.clicked.connect(lambda: set_picker_status(self.model, PickerStatus.NOT_PICKING))

        return frame

    def overlay_options_panel(self) -> QWidget:
        frame = QWidget(self)
        layout = QGridLayout(frame)

        layout.addWidget(QLabel("Overlay options"), 0, 0, 1, 2)

        layout.addWidget(QLabel("Show length lines"), 1, 0, 1, 1)
        show_length_widget = AnimatedToggle(checked_color=CFG.get_hex_color("length-display-style", "color"))
        layout.addWidget(show_length_widget, 1, 1, 1, 1)
        show_length_button = show_length_widget.button
        show_length_button.setChecked(False)

        layout.addWidget(QLabel("Show patient info"), 2, 0, 1, 1)
        show_patient_widget = AnimatedToggle()
        layout.addWidget(show_patient_widget, 2, 1, 1, 1)
        show_patient_button = show_patient_widget.button
        show_patient_button.setChecked(False)

        layout.addWidget(QLabel("Show intermediate pts"), 3, 0, 1, 1)
        show_intermediate_widget = AnimatedToggle()
        layout.addWidget(show_intermediate_widget, 3, 1, 1, 1)
        show_intermediate_button = show_intermediate_widget.button
        show_intermediate_button.setChecked(True)

        layout.addWidget(QLabel("Show pt order"), 4, 0, 1, 1)
        show_ptorder_widget = AnimatedToggle()
        layout.addWidget(show_ptorder_widget, 4, 1, 1, 1)
        show_ptorder_button = show_ptorder_widget.button
        show_ptorder_button.setChecked(False)

        layout.addWidget(QLabel("Comment"), 5, 0, 1, 2)
        layout.addWidget(QPlainTextEdit(), 6, 0, 1, 2)

        return frame

    def centerline(self) -> QWidget:
        frame = QWidget(self)
        layout = QGridLayout(frame)

        layout.addWidget(QLabel("Centerline options"), 0, 0, 1, 2)

        return frame

    def debug(self) -> QWidget:
        frame = QWidget(self)
        layout = QGridLayout(frame)

        layout.addWidget(QLabel("Experimental Features"), 0, 0, 1, 2)

        mpr_pair_pick = AnimatedToggle("Fill MPR between points",
                                       checked_color=CFG.get_hex_color("mpr-display-style", "color"))
        layout.addWidget(mpr_pair_pick, 1, 0, 1, 1)
        mpr_pair_pick_button = mpr_pair_pick.button
        mpr_pair_pick_button.clicked.connect(lambda: set_picker_status(self.model, PickerStatus.PICKING_MPR_PAIR))

        return frame
