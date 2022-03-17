import os
from PyQt5.QtWidgets import QFileDialog

from .ProgressWidget import ProgressWidget
from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


def get_parent_folder():
    fileExplorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
    folderPath = str(fileExplorer.getExistingDirectory())

    if folderPath:
        name = folderPath[folderPath.rfind(os.path.sep) + 1:]
        logging.info(f"Loading {name}")
        return folderPath
    else:
        logging.debug("User canceled/closed file open dialog.")
        raise FileNotFoundError


def get_progress_widget(folder, parent):
    return ProgressWidget(folder, parent)

