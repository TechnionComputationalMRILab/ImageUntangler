from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from collections import namedtuple
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.Viewer.MPRW_Widget import MPRW_Widget
from MPRWindow2.Control.MPRW_Control import MPRW_Control
from MPRWindow2.Model.MPRW_Model import MPRW_Model
import vtk
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRWindow(QDialog):
    """ dialog box for the mpr window """
    def __init__(self, input_data: MPRW_Control):
        super().__init__()

        # self.set_icon()
        # self.set_title()

        # self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        # self.setMinimumSize(QSize(config_data.get_default_width(), config_data.get_default_height()))

        _layout = QVBoxLayout()

        # _mprw_widget = MPRW_Widget(input_data)
        _layout.addWidget(QLabel("aaaaaaaaaaaa"))

        self.setLayout(_layout)
        self.show()

    def set_title(self):
        self.setWindowTitle(config_data.get_config_value("AppName") + ': MPR Window')

    def set_icon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        # self.setWindowTitle("HELLO!")

        # QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        #
        # self.buttonBox = QDialogButtonBox(QBtn)
        #
        # self.layout = QVBoxLayout()
        # message = QLabel("Something happened, is that OK?")
        # # self.layout.addWidget(TestVTKinQFrame().frame)
        # self.layout.addWidget(message)
        # self.layout.addWidget(self.buttonBox)
        # self.setLayout(self.layout)
        # self.show()
        pass