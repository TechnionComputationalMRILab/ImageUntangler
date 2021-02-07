# for testing purposes only
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from MainWindowComponents.TabManager import TabManager


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'TEMP MW'
        self.showMaximized()

        self.table_widget = TabManager(self)
        self.setCentralWidget(self.table_widget)
        self.setStyleSheet("background-color: rgb(68, 71, 79);\n"
                                 "border-color: rgb(0, 0, 0);")

        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())