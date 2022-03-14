from PyQt5.QtWidgets import QFileDialog

from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


def show_preferences_dialog(parent):
    from ..settings.dialog_box import SettingsDialogBox
    logging.debug("Preferences dialog opened")

    preferences = SettingsDialogBox(parent=parent)
    preferences.exec()


def custom_open(parent):
    pass


def bulk_scanner(parent):
    pass


def load_previous_annotation(parent):
    pass


def open_using_file_dialog(parent):
    file_explorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
    folder_path = str(file_explorer.getExistingDirectory())

    if folder_path:
        logging.info(f"Loading from selected folder {folder_path}")
        return folder_path
    else:
        return False
