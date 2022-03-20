from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget
from MRICenterline.gui.display.toolbar import DisplayPanelToolbarButtons
from MRICenterline import CONST


def configure_main_widget(path, parent_widget):
    window = parent_widget.window()
    model = CaseModel(path)

    window.toolbar.addWidget(DisplayPanelToolbarButtons(model=model, parent=window))
    window.setWindowTitle(model.get_case_name() + " | " + CONST.WINDOW_NAME)

    main_display_widget = MainDisplayWidget(model, window)
    window.add_widget(main_display_widget)
