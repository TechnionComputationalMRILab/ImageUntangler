import sqlite3

from MRICenterline.app.points.status import PointStatus
from MRICenterline import CFG


def read_points(pt_id, status: PointStatus):
    con = sqlite3.connect(CFG.get_db())

    if status == PointStatus.MPR:
        points = con.cursor().execute(f"select x, y, z from centerline_coordinates where cl_id='{pt_id}';").fetchall()
    elif status == PointStatus.LENGTH:
        points = con.cursor().execute(f"select x, y, z from length_coordinates where lengths_id='{pt_id}';").fetchall()
    else:
        raise KeyError
    con.close()

    print(points)


print(read_points(1, PointStatus.MPR))
