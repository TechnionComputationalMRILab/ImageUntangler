from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from Model.PointCollection import PointCollection
from View.BaseSequenceViewer import BaseSequenceViewer
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle


class DICOMSliceViewer(BaseSequenceViewer):
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor, interactorStyle: SequenceViewerInteractorStyle, imagePath: str, sliceIdx: int):
        super().__init__(manager, interactor, interactorStyle, imagePath, True)
        self.sliceIdx = sliceIdx
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()
        self.window.Render()

    def processNewPoint(self, pointCollection, pickedCoordinates, color=(1, 0, 0)):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], self.sliceIdx]  # x,y,z,sliceIdx
        if pointCollection.addPoint(pointLocation):
            currentPolygonActor = pointCollection.generatePolygonLastPoint(color)
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(pointCollection)

    def presentPoints(self, pointCollection: PointCollection) -> None:
        for point in pointCollection.points:
            point.polygon.GeneratePolygonOn()
            self.window.Render()






