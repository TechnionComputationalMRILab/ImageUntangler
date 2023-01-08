#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

from MRICenterline import CFG
from MRICenterline.app.database import name_id
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.status import PointStatus


def calculate_total_length(case_id, seq_id, lengths_id):
    if lengths_id:
        con = sqlite3.connect(CFG.get_db())

        itk_points = con.cursor().execute(f"""
                                     select x, y, z
                                     from "length_coordinates"
                                     where lengths_id={lengths_id}
                                     """).fetchall()
        con.close()

        case_path = CFG.get_path_for_case_name(name_id.get_case_name(case_id))

        pt_array = PointArray(PointStatus.LENGTH)

        image_properties = ImageProperties.from_path(case_path, seq_id)

        for itk_pt in itk_points:
            pt = Point.point_from_itk_index(itk_coords=itk_pt, image_properties=image_properties)
            pt_array.add_point(pt)

        return pt_array.total_length
    else:
        return 0


def get_number_of_cl_points(cl_id):
    if cl_id:
        con = sqlite3.connect(CFG.get_db())
        count = con.cursor().execute(f"""
                                     select count(*) 
                                     from "centerline_coordinates"
                                     where cl_id={cl_id}
                                     """).fetchone()
        con.close()

        return count[0]
    else:
        return 0


if __name__ == '__main__': 
    # a = get_number_of_cl_points(1)
    # print(a)

    a = calculate_total_length(case_id=2, seq_id=1, lengths_id=1)
    print(a)
