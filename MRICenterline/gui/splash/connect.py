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
    is_new = check_raw_data_folder(parent)

    if is_new:
        print("new folder")

    else:
        file_open_dialog = FileOpenDialogBox(parent=parent)
        if file_open_dialog.exec():
            selected_file, selected_sequence = file_open_dialog.get_file()
            configure_main_widget(path=str(selected_file), parent_widget=parent, selected_sequence=selected_sequence)


def bulk_scanner(parent):
    from MRICenterline.gui.scanner.widget import ScannerWidget
    check_raw_data_folder(parent)

    window = parent.window()
    window.add_widget(ScannerWidget(window))


def load_previous_annotation(parent):
    from MRICenterline.gui.loader.annotation.dialog_box import AnnotationLoadDialogBox
    from MRICenterline.gui.display.configure import configure_main_widget_from_session

    # check_raw_data_folder(parent)
    db_status = check_database()

    if db_status:
        annotation_load_dialog_box = AnnotationLoadDialogBox(parent=parent)
        if annotation_load_dialog_box.exec():
            selected_session = annotation_load_dialog_box.get_session()
            configure_main_widget_from_session(parent, selected_session)


def open_using_file_dialog(parent):
    from MRICenterline.gui.display.configure import configure_main_widget
    # check_raw_data_folder(parent)

    file_explorer = QFileDialog(directory=CFG.get_config_data("folders", 'data-folder'))
    folder_path = str(file_explorer.getExistingDirectory())

    if folder_path:
        logging.info(f"Loading from selected folder {folder_path}")
        CFG.set_config_data('folders', 'data-folder', folder_path)

        configure_main_widget(path=folder_path, parent_widget=parent)

    else:
        MSG.msg_box_warning("No folder selected.")


def check_raw_data_folder(parent):
    """ if this function returns true, then a new data folder is set and the files need to be pre-processed """

    if CFG.get_folder('raw_data') == 'none':
        from MRICenterline.gui.settings.initial_data_folder_dialog import ask_for_data_folder
        ask_for_data_folder(parent)

        return True
    return False


def check_database():
    """ if this function returns true, there are no cases found in the database """
    import sqlite3
    con = sqlite3.connect(CFG.get_db())
    len_cases = con.cursor().execute("SELECT COUNT(*) FROM CASE_LIST").fetchone()[0]

    if not len_cases:
        MSG.msg_box_warning("No cases found in database.")
        return False
    return True
