import numpy as np
from typing import List
from vtk import vtkRegularPolygonSource, vtkPolyDataMapper, vtkActor


#"""
class Point:
    def __init__(self, coordinates: np.array, polygon: vtkRegularPolygonSource = None):
        self.coordinates = coordinates
        self.polygon = polygon
    
    def addPolygon(self, polygon):
        self.polygon = polygon


class PointCollection:
    def __init__(self):
        self.points: List[Point] = []

    def findImageIndex(self, image: List[int]):
        for i in range(len(self.points)):
            if self.points[i].coordinates == image:
                return i
        return -1

    def addPoint(self, pointLocation: List[int]) -> bool: # x,y,z,sliceIdx
        # returns whether Point was added
        #pointCoordinates = [pointLocation[0], pointLocation[1], pointLocation[2], 0]
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

    @property
    def pointCoordinatesAsList(self):
        return np.asarray([point.coordinates for point in self.points])


#"""

"""
class PointCollection:
    def __init__(self):
        self.points: List[float] = []
        self.polygons = []

    def findImageIndex(self, PointIdImage: np.array) -> int:
        PointIdImage = PointIdImage.tolist()
        print(PointIdImage)
        if PointIdImage in self.points:
            return self.points.index(PointIdImage)
        else:
            return -1

    def addPoint(self, PointIdImage: np.array) -> bool:
        # returns whether Point was added
        imageIndex = self.findImageIndex(PointIdImage)
        if imageIndex == -1:
            self.points.append(PointIdImage.tolist())
            return True
        else:
            return False

    def addPolygon(self, selectedCoordinates, color=(1, 0, 0)) -> vtkActor:
        # returns PolygonActor from generated Polygon. Is assumed that appropiate point already exists
        polygon = vtkRegularPolygonSource()
        polygon.SetCenter((selectedCoordinates[0], selectedCoordinates[1], 0))
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
        self.polygons.append(polygon)
        return polygonActor
"""
