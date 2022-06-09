from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QShortcut
from PyQt5.QtGui import QKeySequence

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.sequence_interactor_widgets import SequenceInteractorWidgets
from MRICenterline.gui.vtk.sequence_interactor_style import SequenceViewerInteractorStyle

from MRICenterline import CFG


class MainDisplayWidget(QWidget):
    def __init__(self, model: CaseModel, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.set_up_keyboard_shortcuts()

        layout = QVBoxLayout(self)

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
