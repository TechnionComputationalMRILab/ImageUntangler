import numpy as np
from typing import List
import vtkmodules.all as vtk


class Point(vtk.vtkActor):
    def __init__(self):
        super().__init__()

