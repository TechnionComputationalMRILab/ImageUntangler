import logging

from PyQt5.QtWidgets import QGroupBox

import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MRICenterline.app.gui_data_handling.gui_imager import GraphicalImager
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties

from MRICenterline.gui.display.sequence_interactor_widgets import SequenceInteractorWidgets
from MRICenterline.gui.vtk.case_widget import CaseWidget


class GenericModel:
    sequence_widgets = None
    vtk_widget = None

    def __init__(self, path):
        self.path = path
        self.image = GraphicalImager(path)

        self.sequence_list = self.image.get_sequences()

        self.active_sequence_index = 0
        self.image_properties: ImageProperties = self.image[self.active_sequence_index]

        self._frame = QGroupBox()
        self.interactor = QVTKRenderWindowInteractor(self._frame)
        self.interactor_style = vtk.vtkInteractorStyleImage()

    ########

    def get_widgets(self, parent_widget):
        self.sequence_widgets = SequenceInteractorWidgets(self, parent_widget)
        self.vtk_widget = CaseWidget(self, self.interactor, self.interactor_style, parent_widget)

        return self.sequence_widgets, self.vtk_widget

    #########
    # callbacks
    #########

    def change_sequence(self, s):
        logging.info(f"Changing sequence to {self.sequence_list[s]}")
        self.active_sequence_index = s
        self.image_properties: ImageProperties = self.image[self.active_sequence_index]

    def change_window(self, v):
        self.sequence_widgets.set_window(v)

    def change_level(self, v):
        self.sequence_widgets.set_level(v)

    def change_index(self, v):
        self.sequence_widgets.set_index(v)

