from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QShortcut
from PyQt5.QtGui import QKeySequence

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.app.points.status import PickerStatus
from MRICenterline.gui.controls.main_panel import ControlPanel
from MRICenterline.gui.display.sequence_interactor_widgets import SequenceInteractorWidgets
from MRICenterline.gui.vtk.sequence_interactor_style import SequenceViewerInteractorStyle
from MRICenterline.gui.display.toolbar_connect import set_picker_status, find_point, edit_points

from MRICenterline import CFG


class MainDisplayWidget(QWidget):
    def __init__(self, model: CaseModel, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.set_up_keyboard_shortcuts()

        layout = QVBoxLayout(self)

        parent.control_panel_dialog.attach_model(model)
        parent.control_panel_dialog.show()
        # self.control_panel_dialog = ControlPanel(self, model)

        self._frame = QGroupBox()
        self.interactor = QVTKRenderWindowInteractor(self._frame)
        self.interactor_style = SequenceViewerInteractorStyle(model=self.model, parent_interactor=self.interactor)

        self.sequence_widgets = SequenceInteractorWidgets(self.model, self)

        self.sequence_manager = self.model.sequence_manager
        self.sequence_viewer = self.sequence_manager.load_sequence(self.model.active_sequence_index,
                                                                   self.interactor,
                                                                   self.interactor_style)

        layout.addLayout(self.sequence_widgets.build_sequence_group_box())
        layout.addWidget(self.interactor)

        if CFG.get_testing_status("show-sliders"):
            layout.addLayout(self.sequence_widgets.build_slider_group_box())

    def test(self):
        self.model.test()

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        self.interactor.Finalize()
        self.control_panel_dialog.close()

    def change_sequence(self, s):
        self.model.change_sequence(s)
        self.sequence_viewer = self.sequence_manager.load_sequence(s, self.interactor, self.interactor_style)
        if CFG.get_testing_status("show-sliders"):
            self.sequence_widgets.initialize_values(slice_index=int(self.sequence_viewer.slice_idx),
                                                    max_slice=self.sequence_viewer.image.size[2],
                                                    window_value=int(self.sequence_viewer.window_val),
                                                    level_value=int(self.sequence_viewer.level_val))

    def change_window(self, v):
        self.sequence_widgets.set_window(v)

    def change_level(self, v):
        self.sequence_widgets.set_level(v)

    def change_index(self, v):
        self.sequence_widgets.set_index(v)

    ########################################
    #             "cheat codes"            #
    ########################################

    def set_up_keyboard_shortcuts(self):
        show_points = QShortcut(QKeySequence('Ctrl+d'), self)
        show_points.activated.connect(self.model.get_points)

        status_command = QShortcut(QKeySequence('Ctrl+q'), self)
        status_command.activated.connect(self.model.print_status_to_terminal)

        save_points = QShortcut(QKeySequence('Ctrl+s'), self)
        save_points.activated.connect(self.model.save)

        overwrite_points = QShortcut(QKeySequence('Ctrl+Shift+s'), self)
        overwrite_points.activated.connect(lambda: print('overwrite'))

        if CFG.get_testing_status("point-shifter"):
            shift_points_ahead = QShortcut(QKeySequence('Ctrl+.'), self)
            shift_points_ahead.activated.connect(lambda: self.model.point_shift("F"))

            shift_points_behind = QShortcut(QKeySequence('Ctrl+,'), self)
            shift_points_behind.activated.connect(lambda: self.model.point_shift("B"))

            reverse_points = QShortcut(QKeySequence('Ctrl+/'), self)
            reverse_points.activated.connect(lambda: self.model.point_shift("R"))

        # TODO: implement these
        # add_mpr_point = QShortcut(QKeySequence('a'), self)
        # add_mpr_point.activated.connect(lambda: set_picker_status(self.model, PickerStatus.PICKING_MPR))
        #
        # find_mpr_point = QShortcut(QKeySequence('s'), self)
        # find_mpr_point.activated.connect(lambda: find_point(self.model, PickerStatus.PICKING_MPR))
        #
        # edit_mpr_point = QShortcut(QKeySequence('e'), self)
        # edit_mpr_point.activated.connect(lambda: edit_points(self.model, PickerStatus.PICKING_MPR))
