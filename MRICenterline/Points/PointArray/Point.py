import numpy as np
import vtkmodules.all as vtk
from icecream import ic


class Point:
    def __init__(self, image_coordinates, color=(1, 0, 0), size=1):
        self.image_coordinates = image_coordinates[0:3]
        self.slice_idx = image_coordinates[-1]
        self.point_color = color
        self.point_size = size if size >= 4 else 4

    def _generate_actor(self):

        source = vtk.vtkSphereSource()
        source.SetCenter(self.image_coordinates[0], self.image_coordinates[1], self.image_coordinates[2])
        source.SetRadius(self.point_size)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # Create an panel_actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(self.point_color)
        actor.GetProperty().SetDiffuse(0.5)
        actor.GetProperty().SetSpecular(0.5)

        return actor

    def get_actor(self):
        return self._generate_actor()

    def set_color(self, color):
        self.point_color = color

    def set_size(self, size):
        self.point_size = size if size >= 4 else 4

    def __sub__(self, other):
        return Point([self.image_coordinates[i] - other[i] for i in range(3)])

    def __add__(self, other):
        return Point([self.image_coordinates[i] + other[i] for i in range(3)])

    def int_div(self, other):
        return Point([self.image_coordinates[i] / other for i in range(3)])

    def distance(self, other):
        return np.sqrt(np.sum([(self.image_coordinates[i] + other[i]) ** 2 for i in range(3)]))

    def __getitem__(self, item):
        return self.image_coordinates[item]

    def __repr__(self):
        return str([i for i in self.image_coordinates])

    def __str__(self):
        return str([i for i in self.image_coordinates])

    def __eq__(self, other):
        return all([self.image_coordinates[i] == other[i] for i in range(3)])

    def __ne__(self, other):
        return not self == other
