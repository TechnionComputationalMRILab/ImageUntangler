import numpy as np
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.status import PointStatus
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties


def fill_interp(image_properties: ImageProperties or None,
                point_a: Point, point_b: Point,
                point_type: PointStatus = PointStatus.MPR,
                num_points: int = 10,
                point_color=(1, 1, 1)) -> PointArray:
    # linearly interpolates the points in the array. used for testing the fill function
    temp_point_array = PointArray(point_type)

    distance = point_a.distance(point_b)
    print(distance)

    x_fill = np.linspace(point_a.image_coordinates[0], point_b.image_coordinates[0], num_points)
    y_fill = np.linspace(point_a.image_coordinates[1], point_b.image_coordinates[1], num_points)

    slice_index = point_a.slice_idx

    pts = [Point(picked_coords=(x, y, 0),
                 slice_index=slice_index,
                 image_properties=image_properties,
                 color=point_color)
           for x, y in zip(x_fill, y_fill)]

    for i, pt in enumerate(pts):
        if i == 0:
            continue
        if i == len(pts) - 1:
            continue
        temp_point_array.add_point(pt)

    temp_point_array.set_color(point_color)
    return temp_point_array


if __name__ == "__main__":
    # start_point = Point(picked_coords=(4.75, -60.67, 0), slice_index=28, image_properties=None)
    # end_point = Point(picked_coords=(24.68, 177.96, 0), slice_index=35, image_properties=None)

    start_point = Point(picked_coords=(4.75, -60.67, 0), slice_index=28, image_properties=None)
    mid_point_1 = Point(picked_coords=(10, 0, 0), slice_index=28, image_properties=None)
    mid_point_2 = Point(picked_coords=(15, 0, 0), slice_index=28, image_properties=None)
    end_point = Point(picked_coords=(24.68, 177.96, 0), slice_index=28, image_properties=None)
    #
    # interp_array = fill_interp(None, start_point, end_point)
    # for i in interp_array:
    #     print(i)

    num_pts = 10
    pa = PointArray(PointStatus.MPR)
    pa.set_use_fill(num_pts)

    pa.add_point(start_point)
    pa.add_point(mid_point_1)
    pa.add_point(mid_point_2)
    pa.add_point(end_point)

    for i, pt in enumerate(pa.interpolated_point_array):
        print(i, pt.image_coordinates)

    print("")

    k = 1
    for i, pt in enumerate(pa.interpolated_point_array[k*(num_pts-2):(num_pts-2)*(k+1)]):
        print(i, pt.image_coordinates)

    print("")

    for i in pa.point_array:
        print(i.image_coordinates)
