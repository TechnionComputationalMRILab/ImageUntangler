from pathlib import Path
from PyQt5.QtWidgets import QFileDialog

from MRICenterline.Config.DialogBox import DialogBox
from MRICenterline import BulkFolderScanner

from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


def show_preferences_dialog(parent):
    logging.debug("Preferences dialog opened")

    _preferences = DialogBox(parent=parent)
    _preferences.exec()


def scan_folders(parent):
    logging.debug("Scanning folders...")

    # try:
    #     _folder = BulkFolderScanner.get_parent_folder()
    # except FileNotFoundError:  # user X-ed out file explorer
    #     return -1
    # else:
    #     _bfs_progress_widget = BulkFolderScanner.get_progress_widget(_folder, parent)
    #     return _bfs_progress_widget


def load_annotations(parent):
    pass


def open_using_file_dialog():
    file_explorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
    folder_path = str(file_explorer.getExistingDirectory())

    if folder_path:
        logging.info(f"Loading from selected folder {folder_path}")
        return folder_path
    else:
        return False


def generate_tab_name(path):
    return str(Path(path)).split("\\")[-2] + " : " + str(Path(path)).split("\\")[-1]