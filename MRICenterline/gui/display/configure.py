from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter

from MRICenterline.app.database import name_id
from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget
from MRICenterline.gui.centerline.widget import CenterlineWidget
from MRICenterline.gui.display.toolbar import DisplayPanelToolbarButtons

from MRICenterline import CONST, CFG


def configure_main_widget(path, parent_widget, selected_sequence=None):
    window = parent_widget.window()
    model = CaseModel(path, selected_sequence)

    splitter = QSplitter(window)
    splitter.setOrientation(Qt.Vertical)

    window.toolbar.addWidget(DisplayPanelToolbarButtons(model=model, parent=window))
    window.setWindowTitle(model.get_case_name() + " | " + CONST.WINDOW_NAME)

    main_display_widget = MainDisplayWidget(model, window)
    centerline_widget = CenterlineWidget(model, window)

    splitter.addWidget(main_display_widget)
    splitter.addWidget(centerline_widget)

    window.add_widget(splitter)


def configure_main_widget_from_session(parent_widget, session_id):
    from MRICenterline.app.database import name_id

    window = parent_widget.window()

    seq_id, case_id, lengths_id, cl_id = name_id.from_session_id(session_id)
    case_name = name_id.get_case_name(case_id)
    seq_name = name_id.get_sequence_name(seq_id, case_id)
    path = Path(CFG.get_folder('raw') + "/" + case_name)

    model = CaseModel(path, seq_name)
    model.load_points(lengths_id, cl_id)

    splitter = QSplitter(window)
    splitter.setOrientation(Qt.Vertical)

    window.toolbar.addWidget(DisplayPanelToolbarButtons(model=model, parent=window))
    window.setWindowTitle(model.get_case_name() + " | " + CONST.WINDOW_NAME)

    main_display_widget = MainDisplayWidget(model, window)
    centerline_widget = CenterlineWidget(model, window)

    splitter.addWidget(main_display_widget)
    splitter.addWidget(centerline_widget)

    window.add_widget(splitter)
