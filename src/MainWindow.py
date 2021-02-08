__author__ = "Yael Zaffrani and Avraham Kahan"

import os, pickle, sys, numpy as np
from typing import List, Tuple
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from MainWindowComponents import MenuBar
from MainWindowComponents.TabManager import TabManager
from util import config_data

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
        self.setStyleSheet("background-color: rgb(68, 71, 79);\n"
                           "border-color: rgb(0, 0, 0);")
        self.buildMenuBar()

    def buildMenuBar(self):
        self.menuBar = MenuBar.getMenuBar()
        self.menuBar.setParent(self)
        self.setMenuBar(self.menuBar)

    def setTitle(self):
        self.setWindowTitle(config_data.get_config_value("AppName"))

    def setIcon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = App()
    MainWindow.show()
    sys.exit(app.exec_())

