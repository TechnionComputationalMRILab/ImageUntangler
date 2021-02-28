import os
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QFileDialog
from util import config_data, stylesheets


class SettingsMenu(QMenu):
    def __init__(self, parent: QMenuBar):
        super().__init__(parent=parent)
        self.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
        self.addDefaultFileOption()

    @staticmethod
    def setDefaultFolder():
        fileExplorer = QFileDialog(directory=config_data.get_config_value('DefaultFolder'))
        folderPath = str(fileExplorer.getExistingDirectory())
        if os.path.exists(folderPath):  # if user picked a directory, ie did not X-out the window
            config_data.update_config_value("DefaultFolder", folderPath)

    def getDefaultFolderAction(self):
        defaultFolderAction = QAction(parent=self)
        defaultFolderAction.triggered.connect(self.setDefaultFolder)
        defaultFolderAction.setText("Select Default Folder")
        return defaultFolderAction

    def addDefaultFileOption(self):
        defaultFolderAction: QAction = self.getDefaultFolderAction()
        self.addAction(defaultFolderAction)
        #self.parent().addAction(self.menuAction())
        self.setTitle("Settings")
