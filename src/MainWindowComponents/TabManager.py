import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTabBar

from MainWindowComponents import Tab


class TabManager(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = Tabs_Bar()
        self.tabs.resize(300, 200)
        self.layout.addWidget(self.tabs)


class Tabs_Bar(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.build_initial_tab()

    def close_tab(self, tab_index):
        if self.count() == 2: # closed last tab
            sys.exit(0)
        currentQWidget = self.widget(tab_index)
        currentQWidget.deleteLater()
        self.removeTab(tab_index)


    def tab_addition(self, tab_index):
        if tab_index == self.count()-1: # last tab clicked
            new_tab = Tab.Tab(parent=self)
            self.insertTab(tab_index, new_tab, new_tab.getName())
            self.setCurrentIndex(tab_index)


    def build_initial_tab(self):
        self.setUpdatesEnabled(True)
        self.insertTab(0, Tab.Tab(parent=self), '    New Tab    ')
        self.insertTab(1, QWidget(), ' + ')
        self.tabBar().setTabButton(1, QTabBar.RightSide, None)
        self.currentChanged.connect(self.tab_addition)



