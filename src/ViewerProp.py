import vtk
import numpy as np
import math
from icecream import ic
from vtk import vtkNrrdReader, vtkDICOMImageReader
from vtk.util import numpy_support


class viewerLogic:
    def __init__(self, mriSeqs, axialImageIndex, coronalImageIndex, isDicom=False):

        self.axialImagePath = mriSeqs[int(axialImageIndex)]
        self.coronalImagePath = mriSeqs[int(coronalImageIndex)]

        self.zoomFactor = 1
        self.SliceIDx =[]

        self.CoronalCenterSliceID = None
        self.AxialCenterSliceID = None

        self.AxialViewer = None # kinda wacky - ViewerProp and AxialCoronalViewer own each other
        self.CoronalViewer = None

        self.CoronalData = self.ReadCoronal(isDicom)
        self.AxialData = self.ReadAxial(isDicom)
        self.LevelVal = (self.CoronalData.dicomArray.max()+self.CoronalData.dicomArray.min())/2
        self.WindowVal = (self.CoronalData.dicomArray.max()-self.CoronalData.dicomArray.min())

        self.CoronalBaseParallelScale = 0.5 * ((self.CoronalData.extent[1] - self.CoronalData.extent[0]) *self.CoronalData.spacing[0])
        self.AxialBaseParallelScale = 0.5 * ((self.AxialData.extent[1] - self.AxialData.extent[0]) * self.AxialData.spacing[0])

    def ReadAxial(self, isDicom: bool):
        if isDicom:
            reader = vtkDICOMImageReader()
        else:
            reader = vtkNrrdReader()
        reader.SetFileName(self.axialImagePath)
        reader.Update()
        axialImageData = reader.GetOutput()
        return ImageProperties(axialImageData, axialImageData.GetSpacing(), axialImageData.GetDimensions(),
                                               axialImageData.GetExtent(), axialImageData.GetPointData(), axialImageData.GetOrigin())


    def ReadCoronal(self, isDicom: bool):
        if isDicom:
            reader = vtkDICOMImageReader()
        else:
            reader = vtkNrrdReader()
        reader.SetFileName(self.coronalImagePath)
        reader.Update()
        coronalImageData = reader.GetOutput()
        return ImageProperties(coronalImageData, coronalImageData.GetSpacing(), coronalImageData.GetDimensions(),
                               coronalImageData.GetExtent(), coronalImageData.GetPointData(), coronalImageData.GetOrigin())
        """
        if np.mod(self.CoronalSliceID, 2) == 0:
            self.CoronalSliceID = int((center_z - self.CoronalData.origin[2]) / self.CoronalVTKSpacing[2] - 0.5)
        else:
            self.CoronalSliceID = int((center_z - self.CoronalData.origin[2]) / self.CoronalVTKSpacing[2])
        """

    def updateZoomFactor(self, ZoomFactor):
        self.zoomFactor = ZoomFactor
        self.AxialViewer.renderer.GetActiveCamera().SetParallelScale(self.AxialBaseParallelScale * ZoomFactor)
        self.AxialViewer.window.Render()
        self.CoronalViewer.renderer.GetActiveCamera().SetParallelScale(self.CoronalBaseParallelScale * ZoomFactor)
        self.CoronalViewer.window.Render()

    def MoveCursor(self, PickerCursorCords, ViewMode: str):
        picking_idx_image = np.zeros(3)
        if ViewMode == 'Axial':
            spacing = self.AxialData.spacing
            shape = np.asarray(self.AxialData.dimensions)
            self.SliceIDx = self.AxialData.sliceID
        elif ViewMode == 'Coronal':
            spacing = self.CoronalData.spacing
            shape = np.asarray(self.CoronalData.dimensions)
            self.SliceIDx = self.CoronalData.sliceID

        viewer_origin = shape / 2.0
        picking_idx_image[2] = self.SliceIDx
        picking_idx_image[0] = PickerCursorCords[0] / spacing[0] + viewer_origin[0]
        picking_idx_image[1] = shape[1] - (PickerCursorCords[1] / spacing[1] + viewer_origin[1])
        picking_idx_image = np.int32(np.round(picking_idx_image))
        axial_curser_coords =self.AxialViewer.Cursor.GetFocalPoint()
        coronal_curser_coords = self.CoronalViewer.Cursor.GetFocalPoint()
        if ViewMode == "Axial":
            # update cursor
            self.AxialViewer.Cursor.SetFocalPoint(PickerCursorCords)
            self.AxialViewer.window.Render()
            coronal_curser_coords = (PickerCursorCords[0], coronal_curser_coords[1], coronal_curser_coords[2])
            self.CoronalViewer.Cursor.SetFocalPoint(coronal_curser_coords)
            # self.CoronalViewer.window.Render()

            newSliceIDx = int(round(self.CoronalDimensions[2] * picking_idx_image[1] / shape[1]))
            center_z = self.CoronalData.origin[2] + newSliceIDx *  self.CoronalData.spacing[2]

            # deltaY = self.CoronalSliceID - round( self.CoronalDimensions[2] * ((shape[1]/2 - picking_idx_image[1])/shape[1]))
            # sliceSpacing = self.CoronalViewer.reslice.GetOutput().GetSpacing()[2]
            self.CoronalViewer.reslice.Update()
            matrix = self.CoronalViewer.reslice.GetResliceAxes()
            # center_z = matrix.GetElement(2, 3) + sliceSpacing * deltaY
            center = (matrix.GetElement(0, 3), matrix.GetElement(1, 3), center_z, 1)
            # sliceIdx = int(round((center[2] - self.CoronalData.origin[2]) / self.CoronalVTKSpacing[2] + 0.5))

            self.CoronalViewer.UpdateViewerMatrixCenter(center, newSliceIDx)

            # # update coronal slice when cursor changes
            # deltaY =  np.int32(self.CoronalSliceID - np.round((self.CoronalDimensions[2]-1) *
            #                                                   picking_idx_image[1]/(self.AxialDimensions[1]-1)))
            # sliceSpacing = self.CoronalViewer.reslice.GetOutput().GetSpacing()[2]
            # matrix = self.CoronalViewer.reslice.GetResliceAxes()
            # center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
            # sliceIdx = int((center[2] - self.CoronalViewer.viewerLogic.CoronalData.origin[2]) /
            #                self.CoronalViewer.viewerLogic.CoronalVTKspacing[2])+1
            # self.CoronalViewer.UpdateViewerMatrixCenter(center, sliceIdx)

        elif ViewMode == "Coronal":
            self.CoronalViewer.Cursor.SetFocalPoint(PickerCursorCords)
            self.CoronalViewer.window.Render()
            axial_curser_coords = (PickerCursorCords[0], coronal_curser_coords[1], coronal_curser_coords[2])
            self.AxialViewer.Cursor.SetFocalPoint(axial_curser_coords)
            self.AxialViewer.Cursor.SetFocalPoint(axial_curser_coords)
            self.AxialViewer.window.Render()


class ImageProperties:
    def __init__(self, fullData, spacing, dimensions, extent, pointData, origin):
        self.fullData = fullData # ??temp
        self.spacing = spacing
        self.dimensions = dimensions
        self.extent = extent
        self.origin = origin
        center_z = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
        self.sliceID = math.ceil((center_z-origin[2]) / spacing[2])
        self.centerSliceID = self.sliceID
        imageData = pointData.GetArray(0)
        ic(imageData)
        self.dicomArray = numpy_support.vtk_to_numpy(imageData)
        self.dicomArray = self.dicomArray.reshape(dimensions, order='F')


