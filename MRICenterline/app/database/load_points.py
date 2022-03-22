import sqlite3

from MRICenterline.app.points.status import PointStatus
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline import CFG


def read_points(pt_id, status: PointStatus, image_properties):
    con = sqlite3.connect(CFG.get_db())

    if status == PointStatus.MPR:
        out_array = PointArray(PointStatus.MPR)
        points = con.cursor().execute(f"select x, y, z from centerline_coordinates where cl_id='{pt_id}';").fetchall()
    elif status == PointStatus.LENGTH:
        out_array = PointArray(PointStatus.LENGTH)
        points = con.cursor().execute(f"select x, y, z from length_coordinates where lengths_id='{pt_id}';").fetchall()
    else:
        raise KeyError
    con.close()

    for pt in points:
        point = Point.point_from_physical(pt, image_properties)
        out_array.add_point(point)

    return out_array
