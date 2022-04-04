import os
import csv
import json
from pathlib import Path
from typing import List
from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from MRICenterline.MainWindow.DefaultTabWidget import DefaultTabWidget
from MRICenterline.MainWindow.CustomOpenDialog import CustomOpenDialog
from MRICenterline.DisplayPanel.Model.GenericModel import GenericModel
from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.Loader.LoadDialog import LoadDirDialog
from MRICenterline.Config.DialogBox import DialogBox
from MRICenterline.MainWindow import MWFunctions
from MRICenterline import BulkFolderScanner

from MRICenterline.Config import CFG
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
        self._case_is_new = True
        self._ldd = None

    def build_new_tab(self):
        logging.debug("Building a new tab")
        self.mainLayout = QHBoxLayout(self)
        self.build_default_tab()

    def build_default_tab(self) -> None:
        self._defaultTabMainWidget = DefaultTabWidget(parent=self)
        self._defaultTabMainWidget.connect_add_mri_images_button(self.load_regular_tab)
        self._defaultTabMainWidget.connect_preferences_button(lambda: MWFunctions.show_preferences_dialog(self))
        self._defaultTabMainWidget.connect_scan_folders_button(self.scan_folders)
        self._defaultTabMainWidget.connect_load_from_json_button(self.json_load)
        self._defaultTabMainWidget.connect_open_mri_from_folder_button(self.open_from_folder)

        self.mainLayout.addWidget(self._defaultTabMainWidget)

    def open_from_folder(self):
        selected_folder = MWFunctions.open_using_file_dialog()
        self._case_is_new = True

        if selected_folder:
            self.load_images_in_pathname(Path(selected_folder))

            tab_name = MWFunctions.generate_tab_name(selected_folder)
            self.finalize_tab_connection(f"Open from FileDialog: {tab_name}")
            self.add_viewers()

        else:
            logging.debug("User canceled/closed file open dialog.")
            self.build_new_tab()

    def scan_folders(self):
        """ initializes the folder scanner widget """
        folder_scanner_widget = MWFunctions.scan_folders(self)

        self.mainLayout.addWidget(folder_scanner_widget)
        self.finalize_tab_connection("Bulk scan")

    def finalize_tab_connection(self, tab_name):
        """ clear the default tab and connects the components to the tab """
        self.mainLayout.removeWidget(self._defaultTabMainWidget)
        self._defaultTabMainWidget.deleteLater()

        self.tab_name = tab_name
        self.Tab_Bar.change_tab_name(self)
        QMetaObject.connectSlotsByName(self)

    def json_load(self):
        logging.debug("Loading from JSON file button clicked")
        pass

        # self._ldd = LoadDirDialog()
        # self._ldd.exec_()
        #
        # if self._ldd.path:
        #     logging.info(f"Opening {self._ldd.path}")
        #
        #     try:
        #         self.load_images_in_pathname(self._ldd.path['path'])
        #     except Exception as e:
        #         logging.error(f"Error in JSON loader: {e}")
        #     else:
        #         self._case_is_new = False
        #         with open(self._ldd.path['full_path'], 'r') as f:
        #             _annotation_file = json.load(f)
        #
        #         self.tab_name = f'{self._ldd.path["file"].strip(".annotation.json")}'
        #         self.clear_default()
        #         self.Tab_Bar.change_tab_name(self)
        #         self.add_viewers(sequence=_annotation_file['SeriesDescription'])
        #         QMetaObject.connectSlotsByName(self)  # connect all components to Tab
        # else:
        #     pass

    def get_name(self):
        return self.tab_name

    def load_images(self):
        pass
        # _open_dlg = CustomOpenDialog()
        # _open_dlg.exec_()
        #
        # # fileExplorer = QFileDialog(directory=CFG.get_config_data("folders", 'default-folder'))
        # # folderPath = str(fileExplorer.getExistingDirectory())
        #
        # _folder_path = _open_dlg.full_path
        # if _folder_path:
        #     self.load_images_in_pathname(Path(_folder_path))
        # else:
        #     logging.debug("User canceled/closed file open dialog.")
        #     self.build_new_tab()
        #     raise FileNotFoundError

    def load_images_in_pathname(self, path):
        self.MRIimages: Imager = Imager(path)
        # self.name = path[path.rfind(os.path.sep) + 1:]
        self.name = str(Path(path)).split("\\")[-2] + " : " + str(Path(path)).split("\\")[-1]
        logging.info(f"Loading {self.name}")
        self.tab_name = os.path.basename(self.name)

    def get_viewer(self, sequence=None):
        try:
            _generic_model = GenericModel(self.MRIimages, parent=self, use_sequence=sequence)
        except Exception as err:
            logging.critical(f"Error in opening file: {err}")
        else:
            if self._case_is_new:
                logging.info("Opening new case")
            else:
                logging.info("Opening point data from file")
                _generic_model.loadAllPoints(self._ldd.path['full_path'])

            return _generic_model

    def add_viewers(self, sequence="None"):
        num_viewers = int(CFG.get_config_data("display", 'horizontal-number-of-panels'))
        logging.debug(f"Adding {num_viewers} viewer(s)")

        for _ in range(num_viewers):
            self.viewerInterfaces.append(self.get_viewer(sequence))
            self.mainLayout.addWidget(self.viewerInterfaces[-1])

    def load_regular_tab(self):
        pass
        # # check if the data directory is present, create it if not
        # _directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'directory.csv')
        #
        # if not os.path.exists(_directory):
        #     logging.info("Directory does not exist, creating...")
        #     with open(_directory, 'w', newline="") as f:
        #         _directory_headers = ['case number', 'sequence name', 'date', '# MPR points', '# len points',
        #                               'Time measurement', 'length', 'path', 'filename']
        #
        #         csv.DictWriter(f, fieldnames=_directory_headers).writeheader()
        # else:
        #     logging.info("Directory found! New savefiles will be appended.")
        #
        # # open file explorer and load selected NRRD images
        # try:
        #     self.load_images()  # load list of images
        # except Exception as e: # user X-ed out file explorer
        #     logging.critical(f"Error in loading tab: {e}")
        #     return -1
        # else:
        #     self.clear_default()
        #     self.Tab_Bar.change_tab_name(self)
        #     self.add_viewers()
        #     QMetaObject.connectSlotsByName(self)  # connect all components to Tab
