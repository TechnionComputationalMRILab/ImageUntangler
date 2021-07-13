from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

import logging
logging.getLogger(__name__)


def create_external_menu_bar():
    _menu_bar = QMenuBar() # parent will be set in MainWindow.py
    _ext_menu = ExternalMenu(_menu_bar)
    _menu_bar.addAction(_ext_menu.menuAction())
    return _menu_bar


class ExternalMenu(QMenu):
    def __init__(self, parent: QMenuBar):
        super().__init__(parent=parent)
        self.set_up_preferences_menu()
        self.set_up_help_menu()

    def help(self):
        logging.debug("Help button clicked")
        print("print help stuff")

    def about(self):
        logging.debug("About button clicked")
        print("about")

    def log(self):
        logging.debug("Log opened")

    def open_help(self):
        _help_action = QAction(parent=self)
        _help_action.triggered.connect(self.help)
        _help_action.setText("Help")
        return _help_action

    def open_about(self):
        _about_action = QAction(parent=self)
        _about_action.triggered.connect(self.about)
        _about_action.setText("About")
        return _about_action

    def open_log(self):
        _about_action = QAction(parent=self)
        _about_action.triggered.connect(self.log)
        _about_action.setText("Control log file")
        return _about_action

    def set_up_help_menu(self):
        self.addAction(self.open_help())
        self.addAction(self.open_about())
        self.addAction(self.open_log())

        self.setTitle("Help")

    def set_up_preferences_menu(self):
        pass
