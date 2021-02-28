__author__ = "Yael Zaffrani and Avraham Kahan"

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from MainWindowComponents import MenuBar
from MainWindowComponents.TabManager import TabManager
from util import config_data, stylesheets

from icecream import ic

ic.configureOutput(includeContext=True)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setIcon()
        self.setTitle()
        self.showMaximized()
        self.tabManager = TabManager(parent=self)
        self.setCentralWidget(self.tabManager)
        self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        self.buildMenuBar()

    def buildMenuBar(self):
        menuBar = MenuBar.buildMenuBar()
        menuBar.setParent(self)
        self.setMenuBar(menuBar)

    def setTitle(self):
        self.setWindowTitle(config_data.get_config_value("AppName"))

    def setIcon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = App()
    MainWindow.show()
    sys.exit(app.exec_())

