from typing import Tuple, List
from vtkmodules.all import vtkTextActor, vtkPolyDataMapper, vtkActor, vtkLineSource

from MRICenterline.app.points.point import Point


class IULineActor(vtkActor):
    def __init__(self, point_a: Point, point_b: Point, color: Tuple[float] = (1, 0, 0), width: float = 2):
        super().__init__()

        pta = [point_a.image_coordinates[0], point_a.image_coordinates[1], 0.0]
        ptb = [point_b.image_coordinates[0], point_b.image_coordinates[1], 0.0]

        line1 = vtkLineSource()
        line1.SetPoint1(*pta)
        line1.SetPoint2(*ptb)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(line1.GetOutputPort())

        self.SetMapper(mapper)
        self.GetProperty().SetColor(*color)
        self.GetProperty().SetLineWidth(width)

    def hide(self):
        self.GetProperty().SetOpacity(0)


class VerticalLine(IULineActor):
    def __init__(self, x_coord: Point or float, color: Tuple[float] = (1, 0, 0), width: float = 2):

        if type(x_coord) is Point:
            coord_a = [x_coord.image_coordinates[0], -10000, 0.0]
            coord_b = [x_coord.image_coordinates[0], 10000, 0.0]
        else:
            coord_a = [x_coord, -10000, 0.0]
            coord_b = [x_coord, 10000, 0.0]

        point_a = Point(coord_a, 0, None)
        point_b = Point(coord_b, 0, None)

        super().__init__(point_a, point_b, color=color, width=width)

    def change_color(self, color: Tuple[float]):
        self.GetProperty().SetColor(*color)


class VerticalLineArray:
    def __init__(self):
        self.line_array: List[VerticalLine] = []

    def add(self, line: VerticalLine):
        self.line_array.append(line)

    def change_color(self, color: Tuple[float]):
        for line in self.line_array:
            line.change_color(color)

    def __getitem__(self, item):
        return self.line_array[item]
