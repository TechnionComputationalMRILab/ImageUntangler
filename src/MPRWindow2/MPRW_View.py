import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from MPRWindow2.MPRW_Control import MPRW_Control
import vtkmodules.all as vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MPRWindow2.MPRInteractor import MPRInteractorStyle
from ast import literal_eval as make_tuple
from icecream import ic
from MPRWindow2.MPRW_ViewerWidget import MPRW_ViewerWidget
from MPRWindow2.MPRW_BottomControls import MPRW_BottomControls
from MPRWindow2.MPRW_Control import MPRW_Control


class MPRW_View(QWidget):
    def __init__(self, model, control, parent=None):
        super(MPRW_View, self).__init__(parent=parent)
        self.model = model
        self.control = control

        self.MPRW_Top = MPRW_ViewerWidget(self.model, self.control, parent=self)
        self.MPRW_Bottom = MPRW_BottomControls(self.model, self.control, parent=self)

    def help_button(self, t):
        # TODO: print some basic help message
        print(t)
        pass
