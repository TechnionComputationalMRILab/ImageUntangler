"""
Exports files from the display panel
"""

import shutil
from PyQt5.QtWidgets import QFileDialog
from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


def export_single_sequence(file_list: list):
    file_explorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
    folder_path = str(file_explorer.getExistingDirectory())

    if folder_path:
        logging.info(f"Saving {len(file_list)} files to {folder_path}")

        for fi in file_list:
            shutil.copy2(src=fi, dst=folder_path)
