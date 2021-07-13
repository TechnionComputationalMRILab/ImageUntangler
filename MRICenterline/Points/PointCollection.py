import numpy as np
from typing import List
from vtkmodules.all import vtkRegularPolygonSource, vtkPolyDataMapper, vtkActor, vtkPoints, vtkPolyData, \
    vtkCellArray, vtkLine, vtkParametricFunctionSource, vtkParametricSpline


class Point:
    def __init__(self, coordinates: np.array, polygon: vtkRegularPolygonSource = None):
        self.coordinates = coordinates
        self.polygon = polygon

    def addPolygon(self, polygon):
        self.polygon = polygon

    def __str__(self):
        return str(self.coordinates)

    def __getitem__(self, item):
        return self.coordinates[item]


class PointCollection:
    def __init__(self):
        self.points: List[Point] = []

    def findImageIndex(self, image: List[int]):
        for i in range(len(self.points)):
            if self.points[i].coordinates == image:
                return i
        return -1

    def addPoint(self, pointLocation: List[int]) -> bool:  # x,y,z,sliceIdx
        # returns whether Point was added
        # pointCoordinates = [pointLocation[0], pointLocation[1], pointLocation[2], 0]
        imageIndex = self.findImageIndex(pointLocation)
        if imageIndex == -1:
            self.points.append(Point(pointLocation))
            return True
        else:
            return False

    def generatePolygonLastPoint(self, color=(1, 0, 0)):
        """adds a polygon for the last added point and returns the polygon"""
        polygon = vtkRegularPolygonSource()
        polygon.SetCenter((self.points[-1].coordinates[0], self.points[-1].coordinates[1], 0))
        polygon.SetRadius(1)
        polygon.SetNumberOfSides(15)
        polygon.GeneratePolylineOff()
        polygon.GeneratePolygonOn()
        polygonMapper = vtkPolyDataMapper()
        polygonMapper.SetInputConnection(polygon.GetOutputPort())
        polygonActor = vtkActor()
        polygonActor.SetMapper(polygonMapper)
        polygonActor.GetProperty().SetColor(color)
        polygonActor.GetProperty().SetAmbient(1)
        self.points[-1].addPolygon(polygon)
        return polygonActor

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]

    def getCoordinatesArray(self) -> np.array:
        return np.asarray([point.coordinates for point in self.points])

    def generateLineActor(self, color=(0, 1, 0), width=4):
        points = self.getCoordinatesArray()[:, 0:3].tolist()

        pts = vtkPoints()
        [pts.InsertNextPoint(i) for i in points]

        linesPolyData = vtkPolyData()
        linesPolyData.SetPoints(pts)

        lineArray = []

        for i in range(len(points)):
            for j in range(len(points)):
                line = vtkLine()
                line.GetPointIds().SetId(0, i)
                line.GetPointIds().SetId(1, j)
                lineArray.append(line)

        lines = vtkCellArray()
        [lines.InsertNextCell(i) for i in lineArray]
        linesPolyData.SetLines(lines)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(linesPolyData)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetLineWidth(width)

        return actor

    def generateSplineActor(self, color=(0, 1, 0), width=4):
        points = self.getCoordinatesArray()[:, 0:3].tolist()

        pts = vtkPoints()
        [pts.InsertNextPoint(i) for i in points]

        outSpline = vtkParametricSpline()
        outSpline.SetPoints(pts)

        functionSource = vtkParametricFunctionSource()
        functionSource.SetParametricFunction(outSpline)

        spline_mapper = vtkPolyDataMapper()
        spline_mapper.SetInputConnection(functionSource.GetOutputPort())

        spline_actor = vtkActor()
        spline_actor.SetMapper(spline_mapper)
        spline_actor.GetProperty().SetColor(color)
        spline_actor.GetProperty().SetLineWidth(width)

        return spline_actor
