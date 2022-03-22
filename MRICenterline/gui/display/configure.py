from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.app.centerline.centerline_model import CenterlineModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget
from MRICenterline.gui.centerline.widget import CenterlineWidget
from MRICenterline.gui.display.toolbar import DisplayPanelToolbarButtons

from MRICenterline import CONST, CFG


def configure_main_widget(path, parent_widget, selected_sequence=None):
    window = parent_widget.window()
    case_model = CaseModel(path, selected_sequence)
    centerline_model = CenterlineModel(case_model)
    case_model.set_centerline_model(centerline_model)

    splitter = QSplitter(window)
    splitter.setOrientation(Qt.Vertical)

    window.toolbar.addWidget(DisplayPanelToolbarButtons(model=case_model, parent=window))
    window.setWindowTitle(case_model.get_case_name() + " | " + CONST.WINDOW_NAME)

    main_display_widget = MainDisplayWidget(case_model, window)
    centerline_widget = CenterlineWidget(centerline_model, window)
    centerline_model.connect_widget(centerline_widget)

    splitter.addWidget(main_display_widget)
    splitter.setStretchFactor(0, 3)

    splitter.addWidget(centerline_widget)
    splitter.setStretchFactor(1, 1)

    window.add_widget(splitter)


def configure_main_widget_from_session(parent_widget, session_id):
    from MRICenterline.app.database import name_id

    window = parent_widget.window()

    seq_id, case_id, lengths_id, cl_id = name_id.from_session_id(session_id)
    case_name = name_id.get_case_name(case_id)
    seq_name = name_id.get_sequence_name(seq_id, case_id)
    path = Path(CFG.get_folder('raw') + "/" + case_name)

    case_model = CaseModel(path, seq_name)
    centerline_model = CenterlineModel(case_model)
    case_model.set_centerline_model(centerline_model)

    main_display_widget = MainDisplayWidget(case_model, window)
    centerline_widget = CenterlineWidget(centerline_model, window)
    centerline_model.connect_widget(centerline_widget)

    case_model.load_points(lengths_id, cl_id)

    splitter = QSplitter(window)
    splitter.setOrientation(Qt.Vertical)

    window.toolbar.addWidget(DisplayPanelToolbarButtons(model=case_model, parent=window))
    window.setWindowTitle(case_model.get_case_name() + " | " + CONST.WINDOW_NAME)

    splitter.addWidget(main_display_widget)
    splitter.setStretchFactor(0, 3)

    splitter.addWidget(centerline_widget)
    splitter.setStretchFactor(1, 1)

    window.add_widget(splitter)
