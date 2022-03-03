import numpy as np
from typing import List
from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.Points.Point import Point
from MRICenterline.Points.LineActor import generate_lines
from MRICenterline.Points.SplineActor import generate_spline
from MRICenterline.Points.LengthCalculation import length_actor, temp_length_calc_function


class PointArray:
    def __init__(self, image: Imager, point_color=(1, 1, 1), size=1, highlight_last=False, highlight_color=(0, 1, 1)):
        self.image = image
        self.itk_index_points: List[Point] = []
        self.physical_points: List[Point] = []
        self.display_points: List[Point] = []
        self.lengths = []
        self.total_length = 0
        self.pt_color = point_color
        self.pt_size = size
        self.highlight_last = highlight_last
        self.highlight_color = highlight_color
        self.hiding_intermediate_points = False

    def get_first_point(self):
        return self[0]

    def get_last_point(self):
        return self[len(self) - 1]

    def __len__(self):
        return len(self.display_points)

    def __getitem__(self, item):
        return self.display_points[item]

    def __iter__(self):
        return iter(self.display_points)

    def delete(self, item):
        self.display_points[item].actor.SetVisibility(False)
        del self.display_points[item]

    def show(self, item):
        self.display_points[item].set_visibility(True)
        self.display_points[item].actor.SetVisibility(True)

    def hide(self, item):
        self.display_points[item].set_visibility(False)
        self.display_points[item].actor.SetVisibility(False)

    def hide_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self)-1:
                self.set_color(color=(0, 0, 1), item=i)
            else:
                self.display_points[i].set_visibility(False)
                self.hide(i)

    def show_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self)-1:
                self.set_color(color=self.pt_color, item=i)
            else:
                self.display_points[i].set_visibility(True)
                self.show(i)

    def addPoint(self, image_point_location):
        # TODO: fix compatibility
        self.add_point(image_point_location)

    def add_point(self, image_point_location):
        viewer_origin = self.image.size / 2.0

        itk_index_x = round(image_point_location[0]/self.image.spacing[0] + viewer_origin[0])
        itk_index_y = round(self.image.size[1] - (image_point_location[1] / self.image.spacing[1] + viewer_origin[1]))
        itk_index_z = image_point_location[2]
        itk_index = (int(itk_index_x), int(itk_index_y), int(itk_index_z))

        if self.highlight_last:
            self.set_color(self.pt_color)

        _new_point_color = self.highlight_color if self.highlight_last else self.pt_color

        self.physical_points.append(Point(self.image.sitk_image.TransformIndexToPhysicalPoint(itk_index)))
        self.itk_index_points.append(Point(itk_index))

        display_pt = Point(image_point_location, color=_new_point_color, size=self.pt_size)
        self.display_points.append(display_pt)

        if len(self) >= 2:
            _temp_length = []
            for i in range(1, len(self.physical_points)):
                _prev_point = self.physical_points[i-1]
                # _temp_length.append((_prev_point, point, point.distance(_prev_point)))
                _temp_length.append(display_pt.distance(_prev_point))
            self.lengths.append(_temp_length[-1])

        self.total_length = sum(self.lengths)

    def show_length_text_actors(self):
        return [length_actor(length) for length in self.lengths]

    def temp_length_display(self):
        # TODO: remove this, use length actors instead
        return [temp_length_calc_function(length) for length in self.lengths]

    def get_actor_list(self):
        return [i.get_actor() for i in self.display_points]

    def get_actor_list_for_slice(self, slice_idx):
        return [i.get_actor() for i in self.display_points if i.slice_idx == slice_idx]

    def displayed_points(self, slice_idx):
        return [i for i in self.display_points if i.slice_idx == slice_idx]

    def hidden_points(self, slice_idx):
        return [i for i in self.display_points if i.slice_idx != slice_idx]

    def set_color(self, color, item=None):
        self.pt_color = color
        try:
            self.display_points[item].set_color(color)
        except (TypeError, IndexError):
            for point in self.display_points:
                point.set_color(color)

    def set_size(self, size, item=None):
        self.pt_size = size
        try:
            self.display_points[item].set_size(size)
        except (TypeError, IndexError):
            for point in self.display_points:
                point.set_size(size)

    def get_line_actor(self, color=(0, 1, 0), width=4):
        return generate_lines(self.display_points, color, width)

    def get_spline_actor(self, color=(0, 1, 0), width=4):
        return generate_spline(self.display_points, color, width)

    def clear_actors(self, renderer):
        _actor_list = self.get_actor_list()
        [renderer.RemoveActor(actor) for actor in _actor_list]

    def get_coordinates_as_array(self) -> np.array:
        return np.asarray([point.image_coordinates for point in self.physical_points])

    def extend(self, point_array):
        self.display_points.extend(point_array.points)
