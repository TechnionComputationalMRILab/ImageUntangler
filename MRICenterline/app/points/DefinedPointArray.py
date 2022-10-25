#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
documentation
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

    def transform(self, point_array: PointArray):
        if len(point_array) <= 2:
            for pt in point_array:
                self.add_point(pt)
        else:
            raise Exception("Can only transform arrays of length 2")


    # def define_start(self, point: Point):
    #     self.start_point = point
    #     self.point_array[0] = point
    #
    #     if self.start_point and self.end_point:
    #         self.fill_out_points()
    #
    # def define_end(self, point: Point):
    #     self.end_point = point
    #     self.point_array[-1] = point
    #
    #     if self.start_point and self.end_point:
    #         self.fill_out_points()

    def fill_out_points(self):
        # TODO: implement the actual fill function here
        print("interpolating")
        self.fill_interp(self.array_length)



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
