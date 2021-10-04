import numpy as np
from typing import List
from MRICenterline.Points.Point import Point
from MRICenterline.Points.LineActor import generate_lines
from MRICenterline.Points.SplineActor import generate_spline
from MRICenterline.Points.LengthCalculation import length_actor, temp_length_calc_function


class PointArray:
    def __init__(self, point_color=(1, 1, 1), size=1, highlight_last=False, highlight_color=(1, 0, 0)):
        self.points: List[Point] = []
        self.lengths = []
        self.pt_color = point_color
        self.pt_size = size
        self.highlight_last = highlight_last
        self.highlight_color = highlight_color

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]

    def __iter__(self):
        return iter(self.points)

    def delete(self, item):
        del self.points[item]

    def addPoint(self, image_point_location):
        # TODO: fix compatibility
        self.add_point(image_point_location)

    def add_point(self, image_point_location):
        if self.highlight_last:
            self.set_color(self.pt_color)

        _new_point_color = self.highlight_color if self.highlight_last else self.pt_color
        _point = Point(image_point_location, color=_new_point_color, size=self.pt_size)
        self.points.append(_point)

        if len(self) >= 2:
            for pt in self.points:
                if _point != pt:
                    self.lengths.append((_point, pt, _point.distance(pt)))

    def show_length_text_actors(self):
        return [length_actor(length) for length in self.lengths]

    def temp_length_display(self):
        #TODO: remove this, use length actors instead
        return [temp_length_calc_function(length) for length in self.lengths]

    def get_actor_list(self):
        return [i.get_actor() for i in self.points]

    def get_actor_list_for_slice(self, slice_idx):
        return [i.get_actor() for i in self.points if i.slice_idx == slice_idx]

    def displayed_points(self, slice_idx):
        return [i for i in self.points if i.slice_idx == slice_idx]

    def hidden_points(self, slice_idx):
        return [i for i in self.points if i.slice_idx != slice_idx]

    def set_color(self, color, item=None):
        self.pt_color = color
        try:
            self.points[item].set_color(color)
        except (TypeError, IndexError):
            for point in self.points:
                point.set_color(color)

    def set_size(self, size, item=None):
        self.pt_size = size
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

    def get_coordinates_as_array(self) -> np.array:
        return np.asarray([point.image_coordinates for point in self.points])

    def extend(self, point_array):
        self.points.extend(point_array.points)
