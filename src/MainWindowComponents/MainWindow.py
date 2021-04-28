__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from MainWindowComponents import InitialMenuBar
from MainWindowComponents.TabManager import TabManager
from util import config_data, stylesheets
import vtkmodules.all as vtk
# from icecream import ic

#ic.configureOutput(includeContext=True)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setIcon()
        self.setTitle()
        # self.showMaximized()
        self.setMinimumSize(QSize(config_data.get_default_width(), config_data.get_default_height()))

        vtk_out = vtk.vtkOutputWindow()
        vtk_out.SetInstance(vtk_out)

        self.tabManager = TabManager(parent=self)
        self.setCentralWidget(self.tabManager)
        self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        self.buildInitialMenuBar()

    def buildInitialMenuBar(self):
        menuBar = InitialMenuBar.buildInitialMenuBar()
        menuBar.setParent(self)
        self.setMenuBar(menuBar)

    def setTitle(self):
        self.setWindowTitle(config_data.get_config_value("AppName") + " v" + config_data.get_config_value("VersionNumber"))

    def setIcon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = App()
    MainWindow.show()
    sys.exit(app.exec_())

