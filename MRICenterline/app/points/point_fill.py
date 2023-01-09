import numpy as np
from enum import Enum

from MRICenterline import CFG
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.status import PointStatus
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.shortest_path.find import FindShortestPathPerSlice


class PointFillType(Enum):
    LinearInterpolation = "linear interp"
    ShortestPath = "shortest path"


def fill_interp(image_properties: ImageProperties or None,
                point_a: Point, point_b: Point,
                point_type: PointStatus = PointStatus.MPR,
                num_points: int = 10) -> PointArray:
    # linearly interpolates the points in the array. used for testing the fill function
    temp_point_array = PointArray(point_type)

    distance = point_a.distance(point_b)
    print(distance)

    x_fill = np.linspace(point_a.image_coordinates[0], point_b.image_coordinates[0], num_points)
    y_fill = np.linspace(point_a.image_coordinates[1], point_b.image_coordinates[1], num_points)

    slice_index = point_a.slice_idx

    pts = [Point(picked_coords=(x, y, 0),
                 slice_index=slice_index,
                 image_properties=image_properties)
           for x, y in zip(x_fill, y_fill)]

    for i, pt in enumerate(pts):
        if i == 0:
            continue
        if i == len(pts) - 1:
            continue
        temp_point_array.add_point(pt)

    temp_point_array.set_color(CFG.get_color('mpr-display-style', 'interpolated-color'))
    return temp_point_array


def fill(image_properties: ImageProperties or None,
         point_a: Point, point_b: Point):
    sitk_image = image_properties.sitk_image

    assert point_a.slice_idx == point_b.slice_idx
    slice_index = point_a.slice_idx

    def convert_coords(pt):
        viewer_origin = image_properties.size / 2.0
        itk_coords = np.zeros(3, dtype=np.int32)

        itk_coords[0] = round((pt.image_coordinates[0] / image_properties.spacing[0]) + viewer_origin[0])
        itk_coords[1] = image_properties.size[1] - round((pt.image_coordinates[1] / image_properties.spacing[1]) + viewer_origin[1])
        itk_coords[2] = round(pt.slice_idx) - 1
        return itk_coords

    shortest_path, _ = FindShortestPathPerSlice(case_sitk=sitk_image, slice_num=point_a.itk_index_coords[2],
                                                first_annotation=convert_coords(point_a),
                                                second_annotation=convert_coords(point_b),
                                                case_number=image_properties.parent.case_name)

    temp_point_array = PointArray(PointStatus.MPR)
    for i, (x, y) in enumerate(zip(shortest_path[0][0], shortest_path[0][1])):
        pt = Point.point_from_itk_index((x, image_properties.size[1] - y, slice_index + 1), image_properties)

        if i == 0:
            continue
        if i == len(shortest_path[0][0]) - 1:
            continue
        temp_point_array.add_point(pt)

    temp_point_array.set_color(CFG.get_color('mpr-display-style', 'interpolated-color'))
    return temp_point_array, len(shortest_path[0][0])


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
