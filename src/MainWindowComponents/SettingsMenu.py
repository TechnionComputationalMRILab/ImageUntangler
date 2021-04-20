import os
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QFileDialog
from util import config_data, stylesheets
from Control.PanelNumberDialog import PanelNumberDialog


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

    @staticmethod
    def setPanelNumber():
        _panel_dialog = PanelNumberDialog()
        _panel_dialog.exec()
        config_data.update_config_value("NumViewers", _panel_dialog.panel_number[0])

    def getDefaultFolderAction(self):
        defaultFolderAction = QAction(parent=self)
        defaultFolderAction.triggered.connect(self.setDefaultFolder)
        defaultFolderAction.setText("Select Default Folder")
        return defaultFolderAction

    def getPanelNumberAction(self):
        defaultPanelNumberAction = QAction(parent=self)
        defaultPanelNumberAction.triggered.connect(self.setPanelNumber)
        defaultPanelNumberAction.setText("Set Number of Panels")
        return defaultPanelNumberAction

    def addDefaultFileOption(self):
        defaultFolderAction: QAction = self.getDefaultFolderAction()
        self.addAction(defaultFolderAction)

        defaultPanelAction: QAction = self.getPanelNumberAction()
        self.addAction(defaultPanelAction)
        self.setTitle("Settings")
