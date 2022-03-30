from typing import Tuple
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
