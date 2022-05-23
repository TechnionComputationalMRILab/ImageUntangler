from typing import List

from MRICenterline.gui.vtk.line_actor import IULineActor
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.status import PointStatus
from MRICenterline import CFG


class PointArray:
    def __init__(self,
                 point_status: PointStatus):
        self.point_type = point_status
        self.point_array: List[Point] = []
        self.lengths: List[float] = []
        self.length_actors = []
        self.total_length: float = 0.0
        self.line_visible = CFG.get_testing_status('draw-connecting-lines')

        if point_status == PointStatus.MPR:
            key = 'mpr-display-style'
        elif point_status == PointStatus.LENGTH:
            key = 'length-display-style'
        elif point_status == PointStatus.LENGTH_IN_MPR:
            key = 'mpr-length-display-style'
        else:
            raise KeyError("Point status not defined")

        self.point_color = CFG.get_color(key, 'color')
        self.point_size = float(CFG.get_config_data(key, 'marker-size'))
        self.highlight_color = CFG.get_color(key, 'highlighted-color')
        self.line_thickness = float(CFG.get_config_data(key, 'line-thickness'))
        self.line_style = CFG.get_config_data(key, 'line-style')

        self.has_highlight = False

    ######################################################################
    #                        array manipulation                          #
    ######################################################################

    def extend(self, point_array):
        for pt in point_array:
            self.add_point(pt)

    def add_point(self, point: Point):
        self.point_array.append(point)
        self.set_size(self.point_size)
        self.set_color(self.point_color)

        if len(self) >= 2:
            self.point_array[-1].set_color(self.highlight_color)

            distance = self.point_array[-2].distance(self.point_array[-1])
            self.lengths.append(distance)
            self.length_actors.append(self.generate_line_actor(self.point_array[-2],
                                                               self.point_array[-1]))
        self.total_length = sum(self.lengths)

    def generate_line_actor(self, point_a, point_b):
        if CFG.get_testing_status('draw-connecting-lines'):
            return IULineActor(point_a, point_b,
                               color=self.point_color,
                               width=self.line_thickness)

    def delete(self, item):
        self.point_array[item].actor.SetVisibility(False)
        self.point_array.pop(item)

        # recalculate lengths
        if len(self):
            if CFG.get_testing_status('draw-connecting-lines'):
                self.length_actors[item].hide()
                self.length_actors.pop(item)

            self.lengths.pop(item)
            self.total_length = sum(self.lengths)

    def clear(self):
        for idx, _ in enumerate(self.point_array):
            self.point_array[idx].actor.SetVisibility(False)

        for idx, _ in enumerate(self.length_actors):
            self.length_actors[idx].hide()

        self.lengths = []
        self.point_array = []
        self.length_actors = []
        self.total_length = 0.0

    ######################################################################
    #                               dunder                               #
    ######################################################################

    def __len__(self):
        return len(self.point_array)

    def __getitem__(self, item):
        return self.point_array[item]

    def __iter__(self):
        return iter(self.point_array)

    def __repr__(self):
        string_list = []
        for pt in self.point_array:
            string = f"slice index {pt.slice_idx} | "\
                     f"image: {pt.image_coordinates} | "\
                     f"itk index: {pt.itk_index_coords} | "\
                     f"physical coords: {pt.physical_coords}"
            string_list.append(string)
        return str(string_list)

    ######################################################################
    #                                 set                                #
    ######################################################################

    def set_size(self, size, item=None):
        self.point_size = size
        if item:
            self.point_array[item].set_size(size)
        else:
            for pt in self.point_array:
                pt.set_size(size)

    def set_color(self, color, item=None):
        self.point_color = color
        if item:
            self.point_array[item].set_color(color)
        else:
            for pt in self.point_array:
                pt.set_color(color)

    ######################################################################
    #                                 get                                #
    ######################################################################

    def get_last_actor(self):
        if len(self) == 1:
            return self.point_array[0].get_actor()
        else:
            return self.point_array[-1].get_actor()

    def get_last_line_actor(self):
        if len(self.length_actors) == 1:
            return self.length_actors[0]
        else:
            return self.length_actors[-1]

    def get_actor_list(self):
        return [i.get_actor() for i in self.point_array]

    def get_line_actors(self):
        return self.length_actors

    def get_spline_actor(self):
        pass
        # return generate_spline(self.point_array, color, width)

    def get_length_for_display(self):
        out_dict = dict()
        for i, length in enumerate(self.lengths):
            out_dict[f'{i}: '] = round(length, 2)
        out_dict['Total Length:'] = round(self.total_length, 2)
        return out_dict

    def get_point_index(self, point: Point) -> int:
        for key, pt in enumerate(self.point_array):
            if pt == point:
                return key

    def get_points_in_slice(self, slice_index: int) -> List[Point]:
        return [pt for pt in self.point_array if slice_index == pt.slice_idx]

    ######################################################################
    #                        actor manipulation                          #
    ######################################################################

    def highlight_specific_point(self, item):
        if self.has_highlight:
            # if a point is already highlighted, set the color of all the points to the point color
            self.set_color(self.point_color)

        self.point_array[item].set_color(self.highlight_color)
        self.has_highlight = True

    def show_point(self, item):
        self.point_array[item].set_visibility(True)
        self.point_array[item].actor.SetVisibility(True)

    def hide_point(self, item):
        self.point_array[item].set_visibility(False)
        self.point_array[item].actor.SetVisibility(False)

    def hide_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self)-1:
                self.set_color(color=self.point_color, item=i)
            else:
                self.point_array[i].set_visibility(False)
                self.hide_point(i)

    def show_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self)-1:
                self.set_color(color=self.point_color, item=i)
            else:
                self.point_array[i].set_visibility(True)
                self.show_point(i)

    def show_for_slice(self, slice_index):
        count = 0
        for i, pt in enumerate(self.point_array):
            if pt.slice_idx == slice_index:
                self.show_point(i)
                count += 1
            else:
                self.hide_point(i)

        return count

    def toggle_line_visibility(self):
        self.line_visible = not self.line_visible
        [actor.SetVisibility(self.line_visible) for actor in self.length_actors]

    ######################################################################
    #                         data point functions                       #
    ######################################################################

    def generate_table_data(self) -> dict:
        img_coords_list = [[round(c, 2) for c in pt.image_coordinates] for pt in self.point_array]
        physical_coords_list = [[round(c, 2) for c in pt.physical_coords] for pt in self.point_array]
        itk_index_list = [[round(c) for c in pt.itk_index_coords] for pt in self.point_array]

        return {
            "physical coords": physical_coords_list,
            "itk indices": itk_index_list,
            "image coords": img_coords_list
        }

    def get_as_np_array(self):
        import numpy as np

        if CFG.get_testing_status("use-slice-location"):
            return np.asarray([pt.image_coordinates for pt in self.point_array])
        else:
            return np.asarray([pt.physical_coords for pt in self.point_array])

    def find_nearest_point(self, other: Point, get_index: bool = False) -> Point or int:
        point_and_distances = []
        for i in self.get_points_in_slice(other.slice_idx):
            point_and_distances.append((other.distance(i), i))

        if get_index:
            return self.get_point_index(sorted(point_and_distances)[0][1])
        else:
            return sorted(point_and_distances)[0][1]

    def get_vertical_distance(self):
        import numpy as np

        points_positions = np.asarray(self.get_as_np_array())
        point_pairs = [(points_positions[j, :], points_positions[j + 1, :]) for j in
                       range(len(points_positions) - 1)]
        vertical_lengths = [np.abs(np.dot((0, 1, 0), i - j)) for i, j in point_pairs]

        return vertical_lengths
