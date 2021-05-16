import os
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from View.DialogLog import DialogLog
from util import stylesheets, logger
logger = logger.get_logger()


class HelpMenu(QMenu):
    def __init__(self, parent: QMenuBar):
        super().__init__(parent=parent)

        self.setStyleSheet(stylesheets.get_sheet_by_name("Menu"))
        self.set_up_help_menu()

    def help(self):
        logger.debug("Help button clicked")
        print("print help stuff")

    def about(self):
        logger.debug("About button clicked")
        print("about")

    def log(self):
        logger.debug("Log opened")
        DialogLog()

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
        _about_action.setText("View log file")
        return _about_action

    def set_up_help_menu(self):
        self.addAction(self.open_help())
        self.addAction(self.open_about())
        self.addAction(self.open_log())

        self.setTitle("Help")
