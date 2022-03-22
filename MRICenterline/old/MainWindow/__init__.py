from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QCloseEvent

from .TabManager import TabManager
from .MenuBar import create_external_menu_bar
from .StatusBar import DisplayPanelStatus

from MRICenterline.Config.InitialConfigBox import InitialConfigDialog
from MRICenterline.utils import program_constants as CONST
from MRICenterline.Config import CFG

from pathlib import Path
import os
import sys
import logging
logging.getLogger(__name__)


class App(QMainWindow):
    def __init__(self, initial_run=False):
        super().__init__()
        logging.info(f"Starting {CONST.APP_NAME}")
        logging.info(f"VERSION {CONST.VER_NUMBER}")
        self.set_icon()
        self.set_title()

        self.check_initial_run(initial_run)

        # make sure that the correct path of IU is in the config file
        CFG.set_config_data('folders', 'image-untangler-folder', Path(str(Path(__file__).parents[2])))

        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))

        if CFG.get_boolean('display', 'start-maximized'):
            self.showMaximized()

        # move VTK warnings/errors to terminal
        vtk_out = vtkOutputWindow()
        vtk_out.SetInstance(vtk_out)

        self.tabManager = TabManager(parent=self)
        self.setCentralWidget(self.tabManager)

        self.build_external_menubar()
        self.setStatusBar(DisplayPanelStatus(parent=self))

    def check_initial_run(self, initial_run):
        if initial_run:
            icd = InitialConfigDialog(self)
            icd_value = icd.exec()

            if icd_value:  # user selected a folder / used the accepted signal
                pass
            else:  # user X'ed out of the dialog box
                sys.exit(0)

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
