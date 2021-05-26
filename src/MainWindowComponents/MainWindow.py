__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from MainWindowComponents import InitialMenuBar
from MainWindowComponents.TabManager import TabManager
import vtkmodules.all as vtk

from util import ConfigRead as CFG, stylesheets, logger
logger.logger_setup()
logger = logger.get_logger()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info(f"Starting {CFG.get_app_name()}")
        logger.info(f"VERSION {CFG.get_version_number()}")
        self.setIcon()
        self.setTitle()
        # self.showMaximized()
        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))

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
        self.setWindowTitle(CFG.get_app_name() + " v" + CFG.get_version_number())

    def setIcon(self):
        self.setWindowIcon(QIcon(CFG.get_icon()))

    def closeEvent(self, a0: QCloseEvent) -> None:
        logger.info("Closing application...")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = App()
    MainWindow.show()
    sys.exit(app.exec_())
