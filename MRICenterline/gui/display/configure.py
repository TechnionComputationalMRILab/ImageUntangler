from MRICenterline.app.gui_data_handling.generic_model import GenericModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget


def configure_main_widget(path, parent_widget):
    window = parent_widget.window()

    model = GenericModel(path)
    main_display_widget = MainDisplayWidget(window)
    sequence_widgets, vtk_widget = model.get_widgets(main_display_widget)

    main_display_widget.configure_widgets(sequence_widgets, vtk_widget)

    window.add_widget(main_display_widget)
