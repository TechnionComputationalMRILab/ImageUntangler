import os
from typing import List
from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from MRICenterline.MainWindow.DefaultTabWidget import DefaultTabWidget
from MRICenterline.DisplayPanel.Model.GenericModel import GenericModel
from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.Config.DialogBox import DialogBox
from MRICenterline import BulkFolderScanner
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.Tab_Bar = parent
        self.name = "New Tab"
        self.tab_name = self.name

        self.viewerInterfaces: List[GenericModel] = []
        self.build_new_tab()

    def build_new_tab(self):
        logging.debug("Building a new tab")
        self.mainLayout = QHBoxLayout(self)  # sets this as layout manager for the tab
        self.build_default_tab()  # builds default tab until user adds regular MRI files

    def build_default_tab(self) -> None:
        self._defaultTabMainWidget = DefaultTabWidget(parent=self)
        self._defaultTabMainWidget.connect_add_mri_images_button(self.load_regular_tab)
        self._defaultTabMainWidget.connect_preferences_button(self.show_preferences_dialog)
        self._defaultTabMainWidget.connect_scan_folders_button(self.scan_folders)
        self._defaultTabMainWidget.connect_load_from_json_button(self.json_load)

        self.mainLayout.addWidget(self._defaultTabMainWidget)

    def scan_folders(self):
        logging.debug("Scanning folders...")

        try:
            _folder = BulkFolderScanner.get_parent_folder()
        except FileNotFoundError: # user X-ed out file explorer
            return -1
        else:
            _bfs_progress_widget = BulkFolderScanner.get_progress_widget(_folder, self)

            self.clear_default()
            self.tab_name = "Bulk scan"
            self.Tab_Bar.change_tab_name(self)
            self.mainLayout.addWidget(_bfs_progress_widget)
            QMetaObject.connectSlotsByName(self)  # connect all components to Tab

    def json_load(self):
        logging.debug("Loading from JSON file button clicked")
        MSG.msg_box_warning("Loading annotations from JSON files is not implemented in this version")

    def show_preferences_dialog(self):
        logging.debug("Preferences dialog opened")
        MSG.msg_box_warning("GUI Preferences editor not implemented in this version",
                            info="Please edit the config.ini using a plain text editor")
        # _preferences = DialogBox(parent=self)
        # _preferences.setWindowModality()

    def get_name(self):
        return self.tab_name
        # if len(self.name) >= 16:
        #     return self.name[:16]
        # else:
        #     padding = 16 - len(self.name)
        #     return "{0}{1}{2}".format(' ' * int(padding/2), self.name, ' ' * int((padding/2) + 0.51))

    def load_images(self):
        fileExplorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
        folderPath = str(fileExplorer.getExistingDirectory())

        if folderPath:
            self.MRIimages: Imager = Imager(folderPath)
            self.name = folderPath[folderPath.rfind(os.path.sep) + 1:]
            logging.info(f"Loading {self.name}")
            self.tab_name = os.path.basename(self.name)

        else:
            logging.debug("User canceled/closed file open dialog.")
            self.build_new_tab()
            raise FileNotFoundError

    def clear_default(self):
        self.mainLayout.removeWidget(self._defaultTabMainWidget)
        self._defaultTabMainWidget.deleteLater()

    def get_viewer(self):
        try:
            return GenericModel(self.MRIimages, parent=self)
        except Exception as err:
            logging.critical(f"Error in opening file: {err}")

    def add_viewers(self):
        num_viewers = int(CFG.get_config_data("display", 'horizontal-number-of-panels'))
        logging.debug(f"Adding {num_viewers} viewer(s)")

        for _ in range(num_viewers):
            self.viewerInterfaces.append(self.get_viewer())
            self.mainLayout.addWidget(self.viewerInterfaces[-1])

    def load_regular_tab(self):
        # open file explorer and load selected NRRD images
        try:
            self.load_images()  # load list of images
        except FileNotFoundError: # user X-ed out file explorer
            return -1
        else:
            self.clear_default()
            self.Tab_Bar.change_tab_name(self)
            self.add_viewers()
            QMetaObject.connectSlotsByName(self)  # connect all components to Tab
