from PyQt5 import QtCore
from PyQt5.QtWidgets import QMenuBar
from util import stylesheets
from MainWindowComponents.SettingsMenu import SettingsMenu


def buildMenuBar():
    # builds MenuBar
    menuBar = QMenuBar() # parent will be set in MainWindow.py
    menuBar.setGeometry(QtCore.QRect(0, 0, 800, 18))  #?# possible portability issue
    menuBar.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
    settingsMenu = SettingsMenu(menuBar)
    menuBar.addAction(settingsMenu.menuAction())
    return menuBar