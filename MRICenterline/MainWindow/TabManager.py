from .Tab import Tab

import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTabBar, QMessageBox, QLabel

import logging
logging.getLogger(__name__)


class TabManager(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        logging.debug("Initializing TabManager")

        # Initialize tab screen
        self.tabs = TabsBar(self)
        self.tabs.resize(300, 200)
        # self.setStyleSheet(stylesheets.get_sheet_by_name("TabManager"))
        self.layout.addWidget(self.tabs)


class TabsBar(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self)
        self.setParent(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.build_initial_tab()

        # self.setCornerWidget(QLabel('test'))

    def build_initial_tab(self):
        logging.debug("Building initial tab")
        self.setUpdatesEnabled(True)
        initial_tab = Tab(parent=self)
        self.insertTab(0, initial_tab, initial_tab.get_name())
        self.insertTab(1, QWidget(), ' + ')
        self.tabBar().setTabButton(1, QTabBar.RightSide, None)
        self.currentChanged.connect(self.tab_addition)

    def close_tab(self, tab_index):
        logging.info("Tab closed")
        if self.count() == 1: # closed last tab
            sys.exit(0)
        currentQWidget = self.widget(tab_index)
        currentQWidget.deleteLater()
        self.removeTab(tab_index)

    def tab_addition(self, tab_index):
        if tab_index == self.count()-1: # '+' button clicked
            logging.info("Tab added")
            new_tab = Tab(parent=self)
            self.insertTab(tab_index, new_tab, new_tab.get_name())
            self.setCurrentIndex(tab_index)

    def change_tab_name(self, tab: Tab):
        tab_index = self.indexOf(tab)
        self.setTabText(tab_index, tab.get_name())
