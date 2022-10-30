#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A PointArray that only takes two points. When the two points are present, an interpolation function
fills out the points in between
"""

import numpy as np

from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.status import PointStatus


class DefinedPointArray(PointArray):
    def __init__(self, array_length: int = 10):

        self.point_count = 0
        # self.point_array = [None] * array_length
        self.array_length = array_length

        super().__init__(point_status=PointStatus.MPR)

    def add_point(self, point: Point):
        super().add_point(point)

        if len(self) == 2:
            self.fill_out_points()
        elif len(self) > 2:
            raise Exception("Cannot add more than two points")

    def transform(self, point_array: PointArray):
        if len(point_array) <= 2:
            for pt in point_array:
                self.add_point(pt)
        else:
            raise Exception("Can only transform arrays of length 2")

    def fill_out_points(self):
        # TODO: implement the actual fill function here
        print("interpolating")
        self.fill_interp(self.array_length)

    def fill_interp(self, num_points: int = 10):
        # the interpolation only works for one direction but it's only for testing anyway
        # linearly interpolates the points in the array. used for testing the fill function
        slice_indices = set([pt.slice_idx for pt in self.point_array if pt])

        # all points in a pt array have the same image_properties by definition
        image_properties = self.point_array[0].image_properties

        if len(slice_indices) == 1:
            idx = slice_indices.pop()
            print("running fill interp")

            # assume all the points are in the same slice

            start = self.point_array[0].image_coordinates[0:2]
            end = self.point_array[-1].image_coordinates[0:2]

            print(start, end)

            x_fill = np.linspace(start[0], end[0], num_points)
            print(x_fill)
            # y_fill = [np.interp(nx, [start[0], end[0]], [start[1], end[1]]) for nx in x_fill]
            y_fill = np.interp(x_fill, [start[0], end[0]], [start[1], end[1]])
            print(y_fill)

            pts = [Point(picked_coords=(x, y, self.point_array[0].image_coordinates[2]),
                         slice_index=idx,
                         image_properties=image_properties)
                   for x, y in zip(x_fill, y_fill)]

            # create a new empty point array with the same point type
            temp_point_array = PointArray(self.point_type)
            for pt in pts:
                temp_point_array.add_point(pt)

            self.point_array = temp_point_array.point_array
            self.lengths = temp_point_array.lengths
            self.length_actors = temp_point_array.length_actors
            self.total_length = temp_point_array.total_length


if __name__ == "__main__":
    dpa = DefinedPointArray()

    start_point = Point(picked_coords=(10, 10, 0), slice_index=1, image_properties=None)
    end_point = Point(picked_coords=(0, 0, 0), slice_index=1, image_properties=None)

    print("define start")
    dpa.add_point(start_point)

    print("define end")
    dpa.add_point(end_point)

    print("points")
    print([i.image_coordinates[0:2] for i in dpa.point_array if i])

    print(len(dpa))

    print("end")
