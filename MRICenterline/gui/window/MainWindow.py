from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget

from MRICenterline.gui.window.Toolbar import IUToolbar
from MRICenterline.gui.splash.InitialWidget import IUInitialWidget

from MRICenterline import CFG


class IUMainWindow(QMainWindow):
    widget_directory = dict()
    EXIT_CODE_REBOOT = -9303635
    singleton: 'IUMainWindow' = None

    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setMinimumSize(QSize(int(CFG.get_config_data('display', 'display-width')),
                                  int(CFG.get_config_data('display', 'display-height'))))
        self.addToolBar(IUToolbar(self))

        if CFG.get_boolean('display', 'start-maximized'):
            self.showMaximized()

        self.main_widget = QStackedWidget(self)
        self.setCentralWidget(self.main_widget)

        self.add_widget(IUInitialWidget(self))

    def add_widget(self, widget: QWidget):
        index = self.main_widget.addWidget(widget)
        self.main_widget.setCurrentIndex(index)
        self.widget_directory[index] = widget
