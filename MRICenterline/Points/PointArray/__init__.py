import numpy as np
from typing import List
import vtkmodules.all as vtk
from .Point import Point
from .LineActor import generate_lines
from .SplineActor import generate_spline
from .LengthCalculation import length_actor


class PointArray:
    def __init__(self):
        self.points: List[Point] = []
        self.lengths = []

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def delete(self, item):
        del self.points[item]

    def addPoint(self, image_point_location):
        # TODO: fix compatibility
        self.add_point(image_point_location)

    def add_point(self, image_point_location):
        self.points.append(Point(image_point_location))

        if len(self) >= 2:
            for pt in self.points:
                if Point(image_point_location) != pt:
                    self.lengths.append((Point(image_point_location), pt, Point(image_point_location).distance(pt)))

    def show_length_text_actors(self):
        return [length_actor(length) for length in self.lengths]

    def get_actor_list(self):
        return [i.get_actor() for i in self.points]

    def get_actor_list_for_slice(self, slice_idx):
        return [i.get_actor() for i in self.points if i.slice_idx == slice_idx]

    def displayed_points(self, slice_idx):
        return [i for i in self.points if i.slice_idx == slice_idx]

    def hidden_points(self, slice_idx):
        return [i for i in self.points if i.slice_idx != slice_idx]

    def set_color(self, color, item=None):
        try:
            self.points[item].set_color(color)
        except (TypeError, IndexError):
            for point in self.points:
                point.set_color(color)

    def set_size(self, size, item=None):
        try:
            self.points[item].set_size(size)
        except (TypeError, IndexError):
            for point in self.points:
                point.set_size(size)

    def get_line_actor(self, color=(0, 1, 0), width=4):
        return generate_lines(self.points, color, width)

    def get_spline_actor(self, color=(0, 1, 0), width=4):
        return generate_spline(self.points, color, width)

    def clear_actors(self, renderer):
        _actor_list = self.get_actor_list()

        [renderer.RemoveActor(actor) for actor in _actor_list]
