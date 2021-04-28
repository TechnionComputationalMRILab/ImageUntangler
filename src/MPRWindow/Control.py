import numpy as np
from typing import List
from Model.getMPR import PointsToPlaneVectors
import vtkmodules.all as vtk
from vtk import vtkImageData


class MPRW_Control:
    def __init__(self, model):
        self.model = model

        self.vtk_image_data = vtkImageData()  # initialize blank image data
        self.actor = vtk.vtkImageActor()

    def get_actor(self):
        self.actor.GetMapper().SetInputData(self.model.calculate_input_data())
        return self.actor
