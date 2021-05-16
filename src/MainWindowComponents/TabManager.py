import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTabBar, QMessageBox

from View.Tab import Tab
from util import stylesheets, logger
logger = logger.get_logger()


class TabManager(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        logger.debug("Initializing TabManager")

        # Initialize tab screen
        self.tabs = Tabs_Bar(self)
        self.tabs.resize(300, 200)
        self.setStyleSheet(stylesheets.get_sheet_by_name("TabManager"))
        self.layout.addWidget(self.tabs)


class Tabs_Bar(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self)
        self.setParent(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.build_initial_tab()

    def close_tab(self, tab_index):
        logger.info("Tab closed")
        if self.count() == 1: # closed last tab
            sys.exit(0)
        currentQWidget = self.widget(tab_index)
        currentQWidget.deleteLater()
        self.removeTab(tab_index)

    def tab_addition(self, tab_index):
        logger.info("Tab added")
        if tab_index == self.count()-1: # '+' button clicked
            new_tab = Tab(parent=self)
            self.insertTab(tab_index, new_tab, new_tab.getName())
            self.setCurrentIndex(tab_index)

    def build_initial_tab(self):
        logger.debug("Building initial tab")
        self.setUpdatesEnabled(True)
        initial_tab = Tab(parent=self)
        self.insertTab(0, initial_tab, initial_tab.getName())
        self.insertTab(1, QWidget(), ' + ')
        self.tabBar().setTabButton(1, QTabBar.RightSide, None)
        self.currentChanged.connect(self.tab_addition)

    def change_tab_name(self, tab: Tab):
        tab_index = self.indexOf(tab)
        self.setTabText(tab_index, tab.getName())
