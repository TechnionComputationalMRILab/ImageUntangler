import os
from typing import List
# from icecream import ic
from PyQt5.QtCore import QMetaObject, QCoreApplication, QRect
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QToolBar, QVBoxLayout

from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from MRICenterline.DisplayPanel.Model.GenericModel import GenericModel
from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.Config import ConfigParserRead as CFG

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
        _defaultTabMainWidget = QWidget(parent=self)
        addFilesButton = QPushButton(_defaultTabMainWidget)
        addFilesButton.setText(QCoreApplication.translate("Tab", "Add MRI Images"))
        addFilesButton.clicked.connect(self.load_regular_tab)  # loads MRI viewer
        addFilesButton.setGeometry(QRect(375, 290, 960, 231))  # TODO should be made more portable

        self.mainLayout.addWidget(_defaultTabMainWidget)

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
        while self.mainLayout.count():
            child = self.mainLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_viewer(self):
        try:
            return GenericModel(self.MRIimages)
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
            # self.clear_default() # TODO: not sure what this is for
            self.Tab_Bar.change_tab_name(self)
            self.add_viewers()
            QMetaObject.connectSlotsByName(self)  # connect all components to Tab
