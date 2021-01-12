import vtk
import numpy as np
import math
from vtk.util import numpy_support


class viewerLogic:
    def __init__(self, FilesList, Setting_Ax, Setting_Co):
        # dict = SeqDic.Dict()
        # AxialSettings = Setting_UL+"_Ax"+"_"+Setting_Ax
        # CoronalSettings = Setting_UL+"_Cor"+"_"+Setting_Co
        # if dict.get(AxialSettings)=="" or dict.get(CoronalSettings)=="":
        #     print("File Not Exist!")
        #     return

        self.AxPath = FilesList[int(Setting_Ax)]
        self.CorPath = FilesList[int(Setting_Co)]
        self.WindowVal = None
        self.LevelVal = None

        self.zoomFactor = 1
        self.SliceIDx =[]

        self.AxialData = []
        self.AxialVTKOrigin =[]
        self.AxialVTKSpacing = []
        self.AxialDimensions = []
        self.AxialSliceID = []
        self.AxialExtent = []
        self.AxialArrayDicom = None


        self.CoronalData = []
        self.CoronalVTKOrigin = []
        self.CoronalVTKSpacing = []
        self.CoronalDimensions = []
        self.CoronalSliceID = []
        self.CoronalExtent = []
        self.CoronalArrayDicom = None

        self.CoronalCenterSliceID = None
        self.AxialCenterSliceID = None

        self.AxialViewer = []
        self.CoronalViewer = []

        # read data
        self.ReadCoronal()
        self.ReadAxial()
        # self.CoronalBaseParallelScale = 0.5 * ((self.CoronalExtent[3] - self.CoronalExtent[2]) *
        #                                        self.CoronalVTKSpacing[1])
        #
        # AxialToCoronalFactor =(self.CoronalExtent[1] *self.CoronalVTKSpacing[0]) /\
        #                            (self.AxialExtent[1] * self.AxialVTKSpacing[0])
        # self.AxialBaseParallelScale = self.CoronalBaseParallelScale / AxialToCoronalFactor
        self.LevelVal = (self.CoronalArrayDicom.max()+self.CoronalArrayDicom.min())/2
        self.WindowVal = (self.CoronalArrayDicom.max()-self.CoronalArrayDicom.min())
        self.CoronalBaseParallelScale = 0.5 * ((self.CoronalExtent[1] - self.CoronalExtent[0]) *self.CoronalVTKSpacing[0])
        self.AxialBaseParallelScale = 0.5 * ((self.AxialExtent[1] - self.AxialExtent[0]) *self.AxialVTKSpacing[0])

    def ReadAxial(self):
        reader = vtk.vtkNrrdReader()
        reader.SetFileName(self.AxPath)
        reader.Update()
        self.AxialData = reader.GetOutput()
        axial_point_data = self.AxialData.GetPointData()
        assert (axial_point_data.GetNumberOfArrays() == 1)
        self.AxialVTKOrigin = self.AxialData.GetOrigin()
        self.AxialVTKSpacing = self.AxialData.GetSpacing()
        self.AxialDimensions = self.AxialData.GetDimensions()
        self.AxialExtent = self.AxialData.GetExtent()
        center_z = self.AxialVTKOrigin[2] + self.AxialVTKSpacing[2] * 0.5 * (self.AxialExtent[4] + self.AxialExtent[5])
        self.AxialSliceID = math.ceil((center_z-self.AxialVTKOrigin[2]) / self.AxialVTKSpacing[2])
        self.AxialCenterSliceID = self.AxialSliceID
        axial_array_data = axial_point_data.GetArray(0)
        self.AxialArrayDicom = numpy_support.vtk_to_numpy(axial_array_data)
        self.AxialArrayDicom = self.AxialArrayDicom.reshape(self.AxialDimensions, order='F')


    def ReadCoronal(self):
        reader = vtk.vtkNrrdReader()
        reader.SetFileName(self.CorPath)
        reader.Update()
        self.CoronalData = reader.GetOutput()
        coronal_point_data = self.CoronalData.GetPointData()
        assert (coronal_point_data.GetNumberOfArrays() == 1)
        self.CoronalVTKOrigin = self.CoronalData.GetOrigin()
        self.CoronalVTKSpacing = self.CoronalData.GetSpacing()
        self.CoronalDimensions = self.CoronalData.GetDimensions()
        self.CoronalExtent = self.CoronalData.GetExtent()
        center_z = self.CoronalVTKOrigin[2] + self.CoronalVTKSpacing[2] * 0.5 * (self.CoronalExtent[4] + self.CoronalExtent[5])
        self.start_center_z = center_z
        # self.CoronalSliceID = math.ceil((center_z - self.CoronalVTKOrigin[2]) / self.CoronalVTKSpacing[2])
        # center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
        # if self.CoronalDimensions[2]
        if np.mod(self.CoronalSliceID,2)==0:
            self.CoronalSliceID = int((center_z - self.CoronalVTKOrigin[2]) / self.CoronalVTKSpacing[2] - 0.5)
        else:
            self.CoronalSliceID = int((center_z - self.CoronalVTKOrigin[2]) / self.CoronalVTKSpacing[2])
        self.CoronalCenterSliceID = self.CoronalSliceID
        coronal_array_data = coronal_point_data.GetArray(0)
        self.CoronalArrayDicom = numpy_support.vtk_to_numpy(coronal_array_data)
        self.CoronalArrayDicom = self.CoronalArrayDicom.reshape(self.CoronalDimensions, order='F')

    def updateZoomFactor(self, ZoomFactor):
        self.zoomFactor = ZoomFactor
        self.AxialViewer.renderer.GetActiveCamera().SetParallelScale(self.AxialBaseParallelScale * ZoomFactor)
        self.AxialViewer.window.Render()
        self.CoronalViewer.renderer.GetActiveCamera().SetParallelScale(self.CoronalBaseParallelScale * ZoomFactor)
        self.CoronalViewer.window.Render()

    def MoveCursor(self, PickerCursorCords, ViewMode):
        picking_idx_image = np.zeros(3)
        if ViewMode == 'Axial':
            spacing = self.AxialVTKSpacing
            shape = np.asarray(self.AxialDimensions)
            self.SliceIDx = self.AxialSliceID
        elif ViewMode == 'Coronal':
            spacing = self.CoronalVTKSpacing
            shape = np.asarray(self.CoronalDimensions)
            self.SliceIDx = self.CoronalSliceID

        viewer_origin = shape / 2.0
        picking_idx_image[2] = self.SliceIDx
        picking_idx_image[0] = PickerCursorCords[0] / spacing[0] + viewer_origin[0]
        picking_idx_image[1] = shape[1] - (PickerCursorCords[1] / spacing[1] + viewer_origin[1])
        picking_idx_image = np.int32(np.round(picking_idx_image))
        # print(picking_idx_image)
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
            center_z = self.CoronalVTKOrigin[2] + newSliceIDx *  self.CoronalVTKSpacing[2]

            # deltaY = self.CoronalSliceID - round( self.CoronalDimensions[2] * ((shape[1]/2 - picking_idx_image[1])/shape[1]))
            # sliceSpacing = self.CoronalViewer.reslice.GetOutput().GetSpacing()[2]
            self.CoronalViewer.reslice.Update()
            matrix = self.CoronalViewer.reslice.GetResliceAxes()
            # center_z = matrix.GetElement(2, 3) + sliceSpacing * deltaY
            center = (matrix.GetElement(0, 3), matrix.GetElement(1, 3), center_z, 1)
            # sliceIdx = int(round((center[2] - self.CoronalVTKOrigin[2]) / self.CoronalVTKSpacing[2] + 0.5))

            self.CoronalViewer.UpdateViewerMatrixCenter(center, newSliceIDx)

            # # update coronal slice when cursor changes
            # deltaY =  np.int32(self.CoronalSliceID - np.round((self.CoronalDimensions[2]-1) *
            #                                                   picking_idx_image[1]/(self.AxialDimensions[1]-1)))
            # sliceSpacing = self.CoronalViewer.reslice.GetOutput().GetSpacing()[2]
            # matrix = self.CoronalViewer.reslice.GetResliceAxes()
            # center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
            # sliceIdx = int((center[2] - self.CoronalViewer.viewerLogic.CoronalVTKOrigin[2]) /
            #                self.CoronalViewer.viewerLogic.CoronalVTKspacing[2])+1
            # self.CoronalViewer.UpdateViewerMatrixCenter(center, sliceIdx)

        elif ViewMode == "Coronal":
            self.CoronalViewer.Cursor.SetFocalPoint(PickerCursorCords)
            self.CoronalViewer.window.Render()
            axial_curser_coords = (PickerCursorCords[0], coronal_curser_coords[1], coronal_curser_coords[2])
            self.AxialViewer.Cursor.SetFocalPoint(axial_curser_coords)
            self.AxialViewer.Cursor.SetFocalPoint(axial_curser_coords)
            self.AxialViewer.window.Render()


        # set new focal points
        '''
        self.AxialViewer.Cursor.SetFocalPoint(axial_curser_coords)
        self.AxialViewer.window.Render()

        self.CoronalViewer.Cursor.SetFocalPoint(CoronalCurserCoords)
        self.CoronalViewer.window.Render()
        '''