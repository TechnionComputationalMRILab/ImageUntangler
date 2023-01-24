from copy import deepcopy
from typing import List


from MRICenterline.app.points.point import Point
from MRICenterline.app.points.status import PointStatus
from MRICenterline import CFG

import logging

logging.getLogger(__name__)


class PointArray:
    def __init__(self,
                 point_status: PointStatus):
        self.point_type = point_status
        self.point_array: List[Point] = []
        self.interpolated_point_array: List[Point] = []
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
        self.highlight_color = CFG.get_color(key, 'highlighted-color')
        self.interpolated_color = None

        self.point_size = float(CFG.get_config_data(key, 'marker-size'))
        self.line_thickness = float(CFG.get_config_data(key, 'line-thickness'))
        self.line_style = CFG.get_config_data(key, 'line-style')

        self.has_highlight = False
        self.highlighted_point = None
        self.use_fill = False
        self.fill_amount = 0
        self.fill_type = None

    ######################################################################
    #                        array manipulation                          #
    ######################################################################
    # region

    def recalculate_array(self, changed_index):
        print(f"previous length: {self.total_length}")
        pt_center = self.point_array[changed_index]

        if changed_index > 0:
            pt_before = self.point_array[changed_index-1]
            d_before = pt_before.distance(pt_center)
            self.lengths[changed_index-1] = d_before
            self.length_actors[changed_index-1] = self.generate_line_actor(pt_before, pt_center)
        else:
            # beginning of array
            # dont want to change value of -1
            pass

        try:
            pt_after = self.point_array[changed_index+1]
            d_after = pt_after.distance(pt_center)
            self.lengths[changed_index] = d_after
            self.length_actors[changed_index] = self.generate_line_actor(pt_center, pt_after)
        except IndexError:
            # end of array
            pass

        self.total_length = sum(self.lengths)
        print(f"new length: {self.total_length}")

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

        if self.use_fill:
            if len(self) >= 2:
                from MRICenterline.app.points.point_fill import fill_interp, PointFillType

                image_properties = self.point_array[0].image_properties

                if self.fill_type == PointFillType.LinearInterpolation:
                    interpolated_array = fill_interp(image_properties=image_properties,
                                                     point_a=self.point_array[-2], point_b=self.point_array[-1],
                                                     point_type=self.point_type,
                                                     num_points=self.fill_amount)
                else:
                    pass
                    # interpolated_array, length_of_fill = fill(image_properties=image_properties,
                    #                                           point_a=self.point_array[-2],
                    #                                           point_b=self.point_array[-1])
                    # self.fill_amount = length_of_fill
                # endregion

                self.interpolated_point_array.extend(interpolated_array)

    def generate_line_actor(self, point_a, point_b):
        from MRICenterline.gui.vtk.line_actor import IULineActor

        if CFG.get_testing_status('draw-connecting-lines'):
            return IULineActor(point_a, point_b,
                               color=self.point_color,
                               width=self.line_thickness)

    def delete(self, item):
        self.point_array[item].actor.SetVisibility(False)
        self.point_array.pop(item)

        if self.use_fill:
            # TODO: incomplete
            self.interpolated_point_array[item].actor.SetVisibility(False)
            for i in range((item)*(self.fill_amount-2), (self.fill_amount-2)*(item+1)):
                del self.interpolated_point_array[i]

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

        if CFG.get_testing_status('draw-connecting-lines'):
            for idx, _ in enumerate(self.length_actors):
                self.length_actors[idx].hide()

        self.lengths = []
        self.point_array = []
        self.length_actors = []
        self.total_length = 0.0

    def shift(self, direction: str):
        logging.debug(f"Array shifted {direction}")

        if direction == "F":
            for pt in self.point_array:
                pt.slice_idx += 1
        elif direction == "B":
            for pt in self.point_array:
                pt.slice_idx -= 1

        return self

    def reverse(self, image_z_size):
        logging.debug("Array reversed")
        for pt in self.point_array:
            pt.slice_idx = image_z_size - pt.slice_idx

        return self

    def edit_point(self, point: Point):
        if self.has_highlight and len(self):
            origin_point = self.highlighted_point

            i = self.get_index(origin_point)
            logging.info(f"Editing point{i}")

            self[i] = point

            return origin_point, i

    # endregion

    ######################################################################
    #                               dunder                               #
    ######################################################################
    # region

    def __len__(self):
        return len(self.point_array)

    def __getitem__(self, item):
        return self.point_array[item]

    def __setitem__(self, key, value):
        # TODO: need to recalculate everything
        self.point_array[key] = value
        self.recalculate_array(key)

    def __iter__(self):
        return iter(self.point_array)

    def __repr__(self):
        string_list = []
        for pt in self.point_array:
            string = f"slice index {pt.slice_idx} | " \
                     f"image: {pt.image_coordinates} | " \
                     f"itk index: {pt.itk_index_coords} | " \
                     f"physical coords: {pt.physical_coords}"
            string_list.append(string)
        return str(string_list)

    # endregion

    ######################################################################
    #                                 set                                #
    ######################################################################
    # region

    def set_use_fill(self, fill_type, fill_amount=10):
        self.use_fill = True
        self.interpolated_color = CFG.get_color('mpr-display-style', 'interpolated-color')
        self.fill_amount = fill_amount
        self.fill_type = fill_type

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

    # endregion

    ######################################################################
    #                                 get                                #
    ######################################################################
    # region

    def get_interpolated_point_actors(self):
        index = len(self)
        return [pt.get_actor()
                for pt in self.interpolated_point_array[(index-2)*(self.fill_amount-2):(self.fill_amount-2)*(index-1)]]

    def get_index(self, point: Point):
        return self.point_array.index(point)

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
            out_dict[f'{i}: '] = f'{round(length, 2)} mm'
        out_dict['Total Length:'] = f'{round(self.total_length, 2)} mm'
        return out_dict

    def get_point_index(self, point: Point) -> int:
        for key, pt in enumerate(self.point_array):
            if pt == point:
                return key

    def get_points_in_slice(self, slice_index: int) -> List[Point]:
        return [pt for pt in self.point_array if slice_index == pt.slice_idx]

    def get_slices_with_points(self) -> List[int]:
        return [pt.slice_idx for pt in self.point_array]

    # endregion

    ######################################################################
    #                        actor manipulation                          #
    ######################################################################
    # region

    def highlight_specific_point(self, item):
        if self.has_highlight:
            # if a point is already highlighted, set the color of all the points to the point color
            self.set_color(self.point_color)

        if len(self):
            self.point_array[item].set_color(self.highlight_color)
            self.has_highlight = True
            self.highlighted_point = self.point_array[item]

            return self.point_array[item].slice_idx

    def show_point(self, item):
        self.point_array[item].set_visibility(True)
        self.point_array[item].actor.SetVisibility(True)

        if self.use_fill:
            for pt_i in self.interpolated_point_array[item*(self.fill_amount-2):(self.fill_amount-2)*(item+1)]:
                pt_i.set_visibility(True)
                pt_i.actor.SetVisibility(True)

    def hide_point(self, item):
        self.point_array[item].set_visibility(False)
        self.point_array[item].actor.SetVisibility(False)

    def hide_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self) - 1:
                self.set_color(color=self.point_color, item=i)
            else:
                self.point_array[i].set_visibility(False)
                self.hide_point(i)

    def show_intermediate_points(self):
        for i in range(len(self)):
            if i == 0 or i == len(self) - 1:
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

    # endregion

    ######################################################################
    #                         data point functions                       #
    ######################################################################
    # region

    def generate_table_data(self) -> dict:
        if self.use_fill:
            img_coords_list = [[round(c, 2) for c in pt.image_coordinates] for pt in self.interpolated_point_array]
            physical_coords_list = [[round(c, 2) for c in pt.physical_coords] for pt in self.interpolated_point_array]
            itk_index_list = [[round(c) for c in pt.itk_index_coords] for pt in self.interpolated_point_array]
        else:
            img_coords_list = [[round(c, 2) for c in pt.image_coordinates] for pt in self.point_array]
            physical_coords_list = [[round(c, 2) for c in pt.physical_coords] for pt in self.point_array]
            itk_index_list = [[round(c) for c in pt.itk_index_coords] for pt in self.point_array]

        return {
            "physical coords": physical_coords_list,
            "itk indices": itk_index_list,
            "image coords": img_coords_list
        }

    def get_as_array_for_centerline(self, image_properties):
        import numpy as np

        if self.use_fill:
            picked_points = deepcopy([pt.itk_index_coords for pt in self.point_array])
            interpolated_points = deepcopy([pt.itk_index_coords for pt in self.interpolated_point_array])

            points = []
            for i, pt in enumerate(picked_points):
                points.append(pt)
                points.extend(interpolated_points[i * (self.fill_amount - 2):(self.fill_amount - 2) * (i + 1)])
        else:
            points = deepcopy([pt.itk_index_coords for pt in self.point_array])

        for i in points:
            i[1] = image_properties.size[1] - i[1]  # flip?
            i[2] = i[2] - 2  # slice index

        return np.asarray(points)

    def find_nearest_point(self, other: Point, get_index: bool = False) -> Point or int:
        point_and_distances = []
        for i in self.get_points_in_slice(other.slice_idx):
            point_and_distances.append((other.distance(i), i))

        if len(self):
            if get_index:
                return self.get_point_index(sorted(point_and_distances)[0][1])
            else:
                return sorted(point_and_distances)[0][1]

    def get_vertical_distance(self):
        import numpy as np

        points_positions = np.asarray([i.image_coordinates for i in self.point_array])
        point_pairs = [(points_positions[j, :], points_positions[j + 1, :]) for j in
                       range(len(points_positions) - 1)]
        vertical_lengths = [np.abs(np.dot((0, 1, 0), i - j)) for i, j in point_pairs]

        return vertical_lengths

    def simplify(self):
        """
        Mostly used for testing if two point arrays are equal by returning only the attributes
        that are relevant for comparison
        """
        simplified_points = list()

        for pt in self.point_array:
            d = dict()
            d['slice_index'] = int(pt.slice_idx)
            d['image_coords'] = pt.image_coordinates
            d["itk_index_coords"] = pt.itk_index_coords
            d['itk_physical_coords'] = pt.physical_coords

            simplified_points.append(d)

        return simplified_points

    # endregion

    ######################################################################
    #                               alias                                #
    ######################################################################
    # region

    def index(self, point: Point):
        return self.get_index(point)

    # endregion
