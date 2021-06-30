import os
from typing import List
from icecream import ic
from PyQt5.QtCore import QMetaObject, QCoreApplication, QRect
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog

from util import ConfigRead as CFG, MRI_files, stylesheets, logger
from MainWindowComponents.MessageBoxes import invalidDirectoryMessage

from Model.NRRDModel import NRRDViewerModel
from Model.DICOMModel import DICOMViewerModel
from Model.GenericModel import GenericModel
from Model.Readers.Imager import Imager

logger = logger.get_logger()
ic.configureOutput(includeContext=True)


class Tab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.Tab_Bar = parent
        self.name = "New Tab"

        if CFG.get_testing_status('reader-reimplementation'):
            self.viewerInterfaces: List[GenericModel] = []
        else:
            self.viewerInterfaces: List[DICOMViewerModel] = []
        self.buildNewTab()

    def getName(self):
        # returns stylized form of name
        if len(self.name) >= 16:
            return self.name[:16]
        else:
            padding = 16 - len(self.name)
            return "{0}{1}{2}".format(' ' * int(padding/2), self.name, ' ' * int((padding/2) + 0.51))

    def loadImages(self):
        fileExplorer = QFileDialog(
            directory=CFG.get_config_data("folders", 'default-folder'))  # opens location to default location
        folderPath = str(fileExplorer.getExistingDirectory())

        if CFG.get_testing_status('reader-reimplementation'):
            self.MRIimages: Imager = Imager(folderPath)
            # TODO: use Imager here
        else:
            self.MRIimages = MRI_files.getMRIimages(folderPath)  # so can be loaded by the viewers

        # this must be set after MRIimages or else tab will be renamed to blank
        # if user X-es out file explorer since error is thrown there
        self.name = folderPath[folderPath.rfind(os.path.sep) + 1:]
        logger.info(f"Loading {self.name}")

    def clearDefault(self):
        while self.mainLayout.count():
            child = self.mainLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_viewer(self):
        try:
            if CFG.get_testing_status('reader-reimplementation'):
                return GenericModel(self.MRIimages)
            else:
                if MRI_files.isValidDicom(self.MRIimages[0]):
                    logger.info("Opening a DICOM file")
                    return DICOMViewerModel(self.MRIimages)
                else:
                    logger.info("Opening a NRRD file")
                    return NRRDViewerModel(self.MRIimages)
        except Exception as err:
            logger.critical(f"Error in opening file: {err}")

    def addViewers(self):
        logger.debug("Adding viewers")
        numViewers = int(CFG.get_config_data("display", 'horizontal-number-of-panels'))
        for _ in range(numViewers):
            self.viewerInterfaces.append(self.get_viewer())
            self.mainLayout.addWidget(self.viewerInterfaces[-1])

    def loadRegularTab(self):
        # open file explorer and load selected NRRD images
        try:
            self.loadImages() # load list of images
        except FileNotFoundError: # user X-ed out file explorer
            return -1

        if CFG.get_testing_status('reader-reimplementation'):
            pass
        else:
            if len(self.MRIimages) < 1:
                invalidDirectoryMessage()
                return -1

        self.clearDefault()
        self.Tab_Bar.change_tab_name(self)
        self.addViewers()
        QMetaObject.connectSlotsByName(self)  # connect all components to Tab

    def setTabProperties(self):
        self.setStyleSheet(stylesheets.get_sheet_by_name("Tab"))

    def buildDefaultTab(self) -> None:
        self.defaultTabMainWidget = QWidget(parent=self)
        addFilesButton = QPushButton(self.defaultTabMainWidget)
        addFilesButton.setText(QCoreApplication.translate("Tab", "Add MRI Images"))
        addFilesButton.setStyleSheet(stylesheets.get_sheet_by_name("AddFiles"))
        addFilesButton.setGeometry(QRect(375, 290, 960, 231))  #EMPHASIS# should be made more portable
        addFilesButton.clicked.connect(self.loadRegularTab)  # loads MRI viewer

        self.mainLayout.addWidget(self.defaultTabMainWidget)

    def buildNewTab(self):
        logger.debug("Building a new tab")
        self.setTabProperties()
        self.mainLayout = QHBoxLayout(self)  # sets this as layout manager for the tab
        self.buildDefaultTab()  # builds default tab until user adds regular MRI files
