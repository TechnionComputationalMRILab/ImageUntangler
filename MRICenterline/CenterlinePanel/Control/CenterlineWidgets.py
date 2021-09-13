from MRICenterline.Points.SaveFormatter import SaveFormatter
import vtkmodules.all as vtk
from vtkmodules.all import vtkImageData

import logging
logging.getLogger(__name__)


class CenterlineWidgets:
    def __init__(self, model):
        logging.debug("Initializing Centerline widgets")
        self.model = model

        self.vtk_image_data = vtkImageData()  # initialize blank image data
        self.actor = vtk.vtkImageActor()

    def get_actor(self):
        self.actor.GetMapper().SetInputData(self.model.calculate_input_data())
        self.actor.GetProperty().SetColorLevel(self.model.interface.level)
        self.actor.GetProperty().SetColorWindow(self.model.interface.window)
        return self.actor

    def save_lengths(self, filename, length_points):
        _save_formatter = SaveFormatter(filename, self.model.image_data)
        _save_formatter.add_pointcollection_data('length in mpr points', length_points)
        _save_formatter.add_generic_data("mpr points", self.model.points)
        _save_formatter.save_data()