import numpy as np
from typing import List
from icecream import ic
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor, vtkRegularPolygonSource, \
    vtkPolyDataMapper, vtkActor, vtkCursor2D
import ViewerProp
from AxialViewerInteractorStyle import AxialViewerInteractorStyle


class PlaneViewerQT:
    def __init__(self, interactor: QVTKRenderWindowInteractor, viewerLogic: ViewerProp.viewerLogic , ViewMode: str):
        self.viewerLogic = viewerLogic
        self.interactor = interactor
        if ViewMode == 'Axial':
            self.imageData = self.viewerLogic.AxialData
            self.viewerLogic.AxialViewer = self
        elif ViewMode == 'Coronal':
            self.imageData = self.viewerLogic.CoronalData
            self.viewerLogic.CoronalViewer = self
        self.sliceIdx = self.imageData.sliceIdx
        self.reslice = vtkImageReslice()
        self.actor = vtkImageActor()
        self.renderer = vtkRenderer()
        self.window: QVTKRenderWindowInteractor = None # intialized in setVtkVols()
        self.interactorStyle = AxialViewerInteractorStyle(parent=self.interactor, baseViewer=self, viewMode=ViewMode)

        self.Cursor = vtkCursor2D()

        self.performReslice()
        self.connectActor()
        self.renderImage()
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()


        self.mprPoints = PointCollection()
        self.lengthPoints = PointCollection()

        self.presentCursor()
        self.window.Render()

    def performReslice(self):
        # Extract a slice in the desired orientation
        x0, y0, z0 = self.imageData.origin
        x_spacing, y_spacing, z_spacing = self.imageData.spacing
        x_min, x_max, y_min, y_max, z_min, z_max = self.imageData.extent

        center = [x0 + x_spacing * 0.5 * (x_min + x_max),
                       y0 + y_spacing * 0.5 * (y_min + y_max),
                       z0 + z_spacing * 0.5 * (z_min + z_max)]
        transformation = vtkMatrix4x4()
        transformation.DeepCopy((1, 0, 0, center[0],
                             0, -1, 0, center[1],
                             0, 0, 1, center[2],
                             0, 0, 0, 1))
        self.reslice.SetInputData(self.imageData.fullData)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

    def connectActor(self):
        self.actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.actor.GetProperty().SetColorWindow(self.viewerLogic.WindowVal)
        self.actor.GetProperty().SetColorLevel(self.viewerLogic.LevelVal)

    def renderImage(self):
        self.renderer.SetBackground(68 / 255, 71 / 255, 79 / 255)
        self.renderer.AddActor(self.actor)
        self.window = self.interactor.GetRenderWindow()
        self.window.AddRenderer(self.renderer)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.window.SetInteractor(self.interactor)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().SetParallelScale(self.imageData.getParallelScale())

    def setIdxText(self):
        self.textActorSliceIdx = vtkTextActor()
        self.textActorSliceIdx.GetTextProperty().SetFontSize(14)
        self.textActorSliceIdx.GetTextProperty().SetColor(1, 250/255, 250/255)
        self.textActorSliceIdx.SetDisplayPosition(0, 2)
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(self.sliceIdx))
        self.renderer.AddActor(self.textActorSliceIdx)

    def setWindowText(self):
        self.textActorWindow = vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(1, 250/255, 250/255)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: " + str(self.viewerLogic.WindowVal))
        self.renderer.AddActor(self.textActorWindow)

    def setLevelText(self):
        self.textActorLevel = vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(1, 250/255, 250/255)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: " + str(self.viewerLogic.LevelVal))
        self.renderer.AddActor(self.textActorLevel)
        self.window.Render()

    def UpdateViewerMatrixCenter(self, center: List[int], sliceIdx):
        ic(sliceIdx)
        matrix = self.reslice.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(sliceIdx))
        self.window.Render()
        self.sliceIdx = sliceIdx
        self.imageData.sliceIdx = sliceIdx
        self.presentPoints(self.mprPoints, sliceIdx)

    def updateWindowAndLevel(self):
        self.viewerLogic.WindowVal = self.actor.GetProperty().GetColorWindow()
        self.viewerLogic.LevelVal = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.viewerLogic.WindowVal)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.viewerLogic.LevelVal)))
        self.window.Render()

    def processNewPoint(self, pointCollection, pickingCoordinates):
        PointIdImage = np.array([pickingCoordinates[0], pickingCoordinates[1], pickingCoordinates[2], self.sliceIdx])  # x,y,z,sliceIdx
        if pointCollection.addPoint(PointIdImage):
            currentPolygonActor = pointCollection.addPolygon(pickingCoordinates)
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(pointCollection, self.sliceIdx)

    def addPoint(self, pointType, PickingCoords):
        if pointType == "MPR":
            self.processNewPoint(self.mprPoints, PickingCoords)
        elif pointType.upper() == "LENGTH":
            self.processNewPoint(self.lengthPoints, PickingCoords)

    def presentPoints(self, pointCollection, sliceIdx) -> None:
        for i in range(len(pointCollection.points)):
            point = pointCollection.points[i]
            polygon = pointCollection.polygons[i]
            if point[3] != sliceIdx: # unclear what case this is
                polygon.GeneratePolygonOff()
            else:
                polygon.GeneratePolygonOn()
            self.window.Render()

    def presentCursor(self):
        self.Cursor.SetModelBounds(-10000, 10000, -10000, 10000, 0, 0)
        self.Cursor.SetFocalPoint(0, 0, 0)
        self.Cursor.AxesOn()
        self.Cursor.TranslationModeOn()
        self.Cursor.OutlineOff()
        cursorMapperAx = vtkPolyDataMapper()
        cursorMapperAx.SetInputConnection(self.Cursor.GetOutputPort())
        cursorActorAx = vtkActor()
        cursorActorAx.SetMapper(cursorMapperAx)
        cursorActorAx.GetProperty().SetColor(1, 0, 0)
        self.renderer.AddActor(cursorActorAx)

    def Start(self):
        self.interactor.Initialize()
        self.interactor.Start()


class PointCollection:
    def __init__(self):
        self.points: List[float] = []
        self.polygons = []

    def findImageIndex(self, PointIdImage: np.array) -> int:
        PointIdImage = PointIdImage.tolist()
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

