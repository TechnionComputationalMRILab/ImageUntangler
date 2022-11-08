from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QToolBar
from PyQt5.QtCore import Qt

from MRICenterline.gui.splash.connect import open_using_file_dialog
from MRICenterline.gui.window.Toolbar import IUToolbar
from MRICenterline.gui.splash.InitialWidget import IUInitialWidget

from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class IUMainWindow(QMainWindow):
    widget_directory = dict()

    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowTitle(CONST.WINDOW_NAME)
        self.setWindowIcon(CFG.get_icon())

        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))
        self.toolbar = IUToolbar(self)
        self.addToolBar(self.toolbar)

        if CFG.get_boolean('display', 'start-maximized'):
            self.showMaximized()

        self.main_widget = QStackedWidget(self)
        self.setCentralWidget(self.main_widget)

        self.add_widget(IUInitialWidget(self))

    def add_widget(self, widget: QWidget):
        index = self.main_widget.addWidget(widget)
        self.main_widget.setCurrentIndex(index)
        self.widget_directory[index] = widget

    def open_new_case(self):
        if len(self.widget_directory) >= 2:
            logging.info("New case button clicked")
            self.main_widget.setCurrentIndex(0)
            self.main_widget.removeWidget(self.widget_directory[1])

            self.removeToolBar(self.toolbar)
            self.toolbar = IUToolbar(self)
            self.addToolBar(self.toolbar)

            self.setWindowTitle(CONST.WINDOW_NAME)

    def open_new_case_from_folder(self):
        open_using_file_dialog(self)
