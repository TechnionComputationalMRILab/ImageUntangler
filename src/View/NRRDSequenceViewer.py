from typing import List
# from icecream import ic
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkMatrix4x4, vtkRenderer, vtkTextActor,  vtkPolyDataMapper,\
    vtkActor, vtkCursor2D

from View.BaseSequenceViewer import BaseSequenceViewer
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from Model.PointCollection import PointCollection
from icecream import ic

from util import logger
logger = logger.get_logger()


class NRRDSequenceViewer(BaseSequenceViewer):
    def __init__(self, manager, interactor: QVTKRenderWindowInteractor, interactorStyle: SequenceViewerInteractorStyle, imagePath: str, isDicom = False):
        super().__init__(manager, interactor, interactorStyle, imagePath, isDicom=False)
        self.sliceIdx = self.imageData.sliceIdx
        self.pastIndex = self.sliceIdx
        self.setIdxText()
        self.setWindowText()
        self.setLevelText()
        self.MPRpoints = PointCollection()
        self.lengthPoints = PointCollection()
        self.presentCursor()

        logger.debug("Rendering sequence")
        self.window.Render()

    def processNewPoint(self, pointCollection, pickedCoordinates, color=(1, 0, 0)):
        pointLocation = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], self.sliceIdx]  # x,y,z,sliceIdx
        self.index_list.append(self.sliceIdx)

        if pointCollection.addPoint(pointLocation):
            currentPolygonActor = pointCollection.generatePolygonLastPoint(color)
            self.renderer.AddActor(currentPolygonActor)
        self.presentPoints(pointCollection, self.sliceIdx)

    # def addPoint(self, pointType, pickedCoordinates):
    #     if pointType.upper() == "MPR":
    #         self.processNewPoint(self.MPRpoints, pickedCoordinates, color=(1, 0, 0))
    #     elif pointType.upper() == "LENGTH":
    #         self.processNewPoint(self.lengthPoints, pickedCoordinates, color=(55/255, 230/255, 128/255))

    def presentPoints(self, pointCollection, sliceIdx) -> None:
        logger.debug("Presenting Points")
        for point in pointCollection.points:
            ic(point)
            polygon = point.polygon
            ic(polygon)
            if point.coordinates[3] != sliceIdx:  # dots were placed on different slices
                print("a")
                polygon.GeneratePolygonOff()
            else:
                print("b")
                polygon.GeneratePolygonOn()
            self.window.Render()

    def processLoadedPoints(self, color=(1, 0, 0)):
        logger.debug(f"Presenting {len(self._loaded_points)} points from file")

        logger.info("CONTINUE HERE")
        # for i in range(len(self._loaded_points)):
        #     logger.debug(f"Adding point {i+1} from file")
        #     # pointLocation = self._loaded_points[i].coordinates + [self._sliceIdx_list[i]]
        #
        #     currentPolygonActor = self._loaded_points.generatePolygonLastPoint(color)
        #     self.renderer.AddActor(currentPolygonActor)
        #     self._loaded_points[i].polygon = currentPolygonActor
        #
        #     self.presentPoints(self._loaded_points, self._sliceIdx_list[i])


    # def presentLoadedPoints(self, pointCollection, slideIdx):
    #
    #
    #     ic(self._loaded_points)
    #     for i in self._loaded_points.points:
    #         pass
    #         # self.addPoint("MPR", tuple(i))
    #     # TODO

    def UpdateViewerMatrixCenter(self, center: List[int], sliceIdx):
        matrix = self.reslice.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(sliceIdx))
        self.window.Render()
        self.sliceIdx = sliceIdx
        self.imageData.sliceIdx = sliceIdx
        self.manager.updateSliderIndex(self.sliceIdx)
        self.presentPoints(self.MPRpoints, sliceIdx)

    def setSliceIndex(self, index: int):
        self.reslice.Update()
        sliceSpacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, (index-self.pastIndex)*sliceSpacing, 1))
        if 0 <= index <= self.imageData.extent[5]:
            self.pastIndex = index
            self.UpdateViewerMatrixCenter(center, index)
        else:
            print("INVALID INDEX ISSUE: PLEASE NOTIFY DEVELOPERS")

    def adjustSliceIdx(self, changeFactor: int):
        # changeFactor determines by how much to change the index
        self.reslice.Update()
        sliceSpacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, changeFactor*sliceSpacing, 1))
        sliceIdx = int((center[2] - self.imageData.origin[2]) /
                       self.imageData.spacing[2] - 0.5)  # z - z_orig/(z_spacing - .5). slice idx is z coordinate of slice of image
        if 0 <= sliceIdx <= self.imageData.extent[5]:
            self.pastIndex = sliceIdx
            self.UpdateViewerMatrixCenter(center, sliceIdx)

