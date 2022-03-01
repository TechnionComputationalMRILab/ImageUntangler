from shutil import copy
import os
from glob import glob
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout
from PyQt5.Qt import Qt

from MRICenterline.Config.PreferencesWidget import PreferencesWidget
from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


class DialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.preferences_widget = PreferencesWidget(parent=self)
        self.setWindowTitle("Preferences")

        _buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel | \
                   QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Help

        self.button_box = QDialogButtonBox(_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.helpRequested.connect(self.help)
        self.button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.reset)

        self.button_box.setOrientation(Qt.Vertical)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.preferences_widget)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.setMinimumWidth(1000)

    def accept(self) -> None:
        logging.info("Preferences: Accept function")

        # folders
        CFG.set_config_data('folders', 'default-folder', self.preferences_widget.default_folder)

        # display
        CFG.set_color_data('display', self.preferences_widget.panel_text_color)
        CFG.set_config_data('display', 'horizontal-number-of-panels', self.preferences_widget.hpanel_number)

        # length_display_style
        CFG.set_color_data('length-display-style', self.preferences_widget.length_color)

        # centerline_style
        CFG.set_color_data('mpr-display-style', self.preferences_widget.centerline_color)

        # testing
        CFG.set_config_data('testing', 'show-fixer-button', self.preferences_widget.testing_show_fixer)

        super().accept()

    def reject(self) -> None:
        logging.info("Preferences: Reject function")
        super().reject()

    def help(self):
        logging.info("Preferences: Help function")

    def reset(self) -> None:
        logging.info("Preferences: Reset function")

        _default_config = [file.replace('\\', '/')
                           for file in glob(f"{os.getcwd()}/**/default_config.ini", recursive=True)][0]
        _config_file = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')
        copy(_default_config, _config_file)

        super().accept()