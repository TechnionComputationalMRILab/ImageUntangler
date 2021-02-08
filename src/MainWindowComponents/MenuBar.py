import os
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QFileDialog
from util import config_data, stylesheets


def getMenuBar():
    menuBar: QMenuBar = buildMenuBar()
    return menuBar


def setDefaultFolder():
    fileExplorer = QFileDialog(directory=config_data.get_config_value('DefaultFolder'))
    folderPath = str(fileExplorer.getExistingDirectory())
    if os.path.exists(folderPath): # assumed to be always true since is picked with file dialog
        config_data.update_config_value("DefaultFolder", folderPath)


def getDefaultFolderAction(settingsTab):
    defaultFolderAction = QAction(parent=settingsTab)
    defaultFolderAction.triggered.connect(setDefaultFolder)
    defaultFolderAction.setText(QCoreApplication.translate("MainWindow", "Select Default Folder"))
    return defaultFolderAction


def addSettingsMenu(menuBar: QMenuBar) -> None:
    settingsMenu = QMenu(parent=menuBar)
    #settingsMenu.setStyleSheet("""QMenu { background-color: rgb(236, 232, 232); }""")
    settingsMenu.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
    defaultFolderAction = getDefaultFolderAction(settingsMenu)
    settingsMenu.addAction(defaultFolderAction)
    menuBar.addAction(settingsMenu.menuAction())
    settingsMenu.setTitle(QCoreApplication.translate("MainWindow", "Settings"))

def addDotActions():
    pass

def addDotMenu(menuBar: QMenuBar) -> None:
    dotMenu = QMenu(parent=menuBar)
    dotMenu.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
    addDotActions(dotMenu)
    menuBar.addActions(dotMenu.menuAction())
    dotMenu.setTitle(QCoreApplication.translate("MainWindow", "Set Dots"))

def buildMenuBar():
    # builds MenuBar
    menuBar = QMenuBar() # parent will be set in OldMainWindow.py
    menuBar.setGeometry(QtCore.QRect(0, 0, 800, 18))
    #menuBar.setStyleSheet("""QMenuBar { background-color: rgb(236, 232, 232); }""")
    menuBar.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
    addSettingsMenu(menuBar) # adds setting option in menubar
    return menuBar