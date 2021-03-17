from PyQt5.QtCore import QRect, QSize, QCoreApplication, QMetaObject
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QSizePolicy, QVBoxLayout, QPushButton, QLabel,QDoubleSpinBox, \
    QMenuBar, QSpinBox, QStatusBar, QFileDialog, QMainWindow, QApplication, QDialog, QToolBar, QHBoxLayout
import numpy as np
from collections import namedtuple
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.Viewer.MPRW_Widget import MPRW_Widget

import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRWindow(QDialog):
    def __init__(self, MPR_M, delta, MPRposition, points):
        super().__init__()
        self.setIcon()
        self.setTitle()
        self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))

        self.MPR_M = MPR_M
        self.delta = delta
        self.MPRposition = MPRposition
        self.points = points

        self.resize(990, 797)  # TODO: rewrite this programatically
        self.setMaximumSize(QSize(990, 16777215))  # TODO: rewrite this programatically

        _layout = QVBoxLayout()
        _mprw_widget = MPRW_Widget()
        _layout.addWidget(_mprw_widget)
        self.setLayout(_layout)

        self.exec_()

    def setTitle(self):
        self.setWindowTitle(config_data.get_config_value("AppName") + ': MPR Window')

    def setIcon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))


if __name__ == "__main__":
    app = QApplication([])
    MPRWindow = MPRWindow()
    MPRWindow.show()
    sys.exit(app.exec_())
