from pathlib import Path

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow

from .Toolbar import IUToolbar
from ..splash.InitialWidget import IUInitialWidget
from MRICenterline.Config import CFG


class IUMainWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None, initial_run=True):
        """Initializer."""
        super().__init__(parent)

        # make sure that the correct path of IU is in the config file
        CFG.set_config_data('folders', 'image-untangler-folder', Path(str(Path(__file__).parents[2])))

        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))

        if CFG.get_boolean('display', 'start-maximized'):
            self.showMaximized()

        self.centralWidget = IUInitialWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.addToolBar(IUToolbar(self))
