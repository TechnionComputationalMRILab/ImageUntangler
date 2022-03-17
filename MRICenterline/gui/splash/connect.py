from PyQt5.QtWidgets import QFileDialog

from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


def show_preferences_dialog(parent):
    from MRICenterline.gui.settings.dialog_box import SettingsDialogBox
    logging.debug("Preferences dialog opened")

    preferences = SettingsDialogBox(parent=parent)
    preferences.exec()


def custom_open(parent):
    """ opens the custom open dialog """
    from MRICenterline.gui.loader.file.dialog_box import FileOpenDialogBox
    from MRICenterline.gui.display.configure import configure_main_widget
    check_raw_data_folder(parent)

    file_open_dialog = FileOpenDialogBox(parent=parent)
    if file_open_dialog.exec():
        selected_file = file_open_dialog.get_file()
        configure_main_widget(path=selected_file, parent_widget=parent)


def bulk_scanner(parent):
    from MRICenterline.gui.scanner.widget import ScannerWidget
    check_raw_data_folder(parent)

    window = parent.window()
    window.add_widget(ScannerWidget(window))


def load_previous_annotation(parent):
    from MRICenterline.gui.loader.annotation.dialog_box import AnnotationLoadDialogBox
    check_database()

    annotation_load_dialog_box = AnnotationLoadDialogBox(parent=parent)
    if annotation_load_dialog_box.exec():
        # build build build
        pass


def open_using_file_dialog(parent):
    from MRICenterline.gui.display.configure import configure_main_widget
    check_raw_data_folder(parent)

    file_explorer = QFileDialog(directory=CFG.get_config_data("folders", 'data-folder'))
    folder_path = str(file_explorer.getExistingDirectory())

    if folder_path:
        logging.info(f"Loading from selected folder {folder_path}")

        configure_main_widget(path=folder_path, parent_widget=parent)

    else:
        MSG.msg_box_warning("No folder selected.")


def check_raw_data_folder(parent):
    if CFG.get_folder('raw_data') == 'none':
        from MRICenterline.gui.settings.initial_data_folder_dialog import ask_for_data_folder
        ask_for_data_folder(parent)


def check_database():
    pass
