import numpy as np
import math
from typing import List
from icecream import ic
from vtk import vtkNrrdReader, vtkDICOMImageReader
from vtk.util import numpy_support


class viewerLogic:
    def __init__(self, mriSeqs: List[str], axialImageIndex: str, coronalImageIndex: str, isDicom=False):
        self.zoomFactor = 1

        self.AxialViewer = None
        self.CoronalViewer = None

        coronalImagePath = mriSeqs[int(coronalImageIndex)]
        self.CoronalData = self.getImageData(coronalImagePath, isDicom)

        axialImagePath = mriSeqs[int(axialImageIndex)]
        self.AxialData = self.getImageData(axialImagePath, isDicom)

        self.LevelVal = (self.CoronalData.dicomArray.max()+self.CoronalData.dicomArray.min())/2
        self.WindowVal = (self.CoronalData.dicomArray.max()-self.CoronalData.dicomArray.min())

    @staticmethod
    def getImageData(imgPath: str, isDicom: bool):
        if isDicom:
            reader = vtkDICOMImageReader()
        else:
            reader = vtkNrrdReader()
        reader.SetFileName(imgPath)
        reader.Update()
        imageData = reader.GetOutput()
        return ImageProperties(imageData, imageData.GetSpacing(), imageData.GetDimensions(),
                                               imageData.GetExtent(), imageData.GetPointData(), imageData.GetOrigin())

    def updateZoomFactor(self, ZoomFactor):
        self.zoomFactor = ZoomFactor
        self.AxialViewer.renderer.GetActiveCamera().SetParallelScale(self.AxialData.getParallelScale() * ZoomFactor)
        self.AxialViewer.window.Render()
        self.CoronalViewer.renderer.GetActiveCamera().SetParallelScale(self.CoronalData.getParallelScale() * ZoomFactor)
        self.CoronalViewer.window.Render()

    def moveBullsEye(self, PickerCursorCords, ViewMode: str):
        # called when moving bulls eye
        if ViewMode == "Axial":
            self.AxialViewer.Cursor.SetFocalPoint(PickerCursorCords)
            self.AxialViewer.window.Render()

        elif ViewMode == "Coronal":
            self.CoronalViewer.Cursor.SetFocalPoint(PickerCursorCords)
            self.CoronalViewer.window.Render()


class ImageProperties:
    def __init__(self, fullData, spacing, dimensions, extent, pointData, origin):
        self.fullData = fullData # ??temp
        self.spacing = spacing
        self.dimensions = dimensions
        self.extent = extent
        self.origin = origin
        center_z = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
        self.sliceIdx = math.ceil((center_z-origin[2]) / spacing[2])
        nn = pointData.GetArray(0)
        self.dicomArray = numpy_support.vtk_to_numpy(nn)
        self.dicomArray = self.dicomArray.reshape(dimensions, order='F')

    def getParallelScale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])


