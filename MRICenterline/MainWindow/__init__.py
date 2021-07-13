from MRICenterline.utils import program_constants as CONST
from MRICenterline.Config import ConfigParserRead as CFG
from .TabManager import TabManager
from .MenuBar import create_external_menu_bar
from .StatusBar import DisplayPanelStatus

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QCloseEvent
import vtkmodules.all as vtk

import os
from pathlib import Path
import logging
logging.getLogger(__name__)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info(f"Starting {CONST.APP_NAME}")
        logging.info(f"VERSION {CONST.VER_NUMBER}")
        self.set_icon()
        self.set_title()
        self.showMaximized()
        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))

        # move VTK warnings/errors to terminal
        vtk_out = vtk.vtkOutputWindow()
        vtk_out.SetInstance(vtk_out)

        self.tabManager = TabManager(parent=self)
        self.setCentralWidget(self.tabManager)

        self.build_external_menubar()
        self.setStatusBar(DisplayPanelStatus(parent=self))

    def build_external_menubar(self):
        _ext_mb = create_external_menu_bar()
        _ext_mb.setParent(self)
        self.setMenuBar(_ext_mb)

    def set_title(self):
        self.setWindowTitle(CONST.APP_NAME +
                            " by " + CONST.APP_BYLINE +
                            " v" + CONST.VER_NUMBER)

    def set_icon(self):
        _icon_path = os.path.join('static', CONST.LAB_ICON)
        self.setWindowIcon(QIcon(_icon_path))

    def closeEvent(self, a0: QCloseEvent) -> None:
        logging.info("Closing application...")
