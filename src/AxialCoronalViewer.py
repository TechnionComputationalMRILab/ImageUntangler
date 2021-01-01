import vtk
import AxialViewerInteractorStyle
import numpy as np

class PlaneViewerQT():

    # ZminVTK: object

    def __init__(self, interactor, viewerLogic, ViewMode):
        self.viewerLogic = viewerLogic
        self.interactor = interactor
        # self.visualizationWindow = self.viewerLogic.WindowVal
        # self.visualizationLevel = self.viewerLogic.LevelVal
        self.ViewMode = ViewMode
        if self.ViewMode == 'Axial':
            self.SliceIDx = self.viewerLogic.AxialSliceID
        elif self.ViewMode == 'Coronal':
            self.SliceIDx = self.viewerLogic.CoronalSliceID

        self.vtkVol = []
        self.center = []
        self.axial = []
        self.coronal = []
        self.sagittal = []
        self.reslice = []
        self.actor = []
        self.renderer = []
        self.window = []
        self.interactorStyle = []
        self.PointList =[]
        self.Cursor = []
        self.StartCenter = []
        self.ZminVTK = None
        self.ZmaxVTK = None

        self.PickingPointsIm = []
        self.PickingPointVTK = []
        self.polygonList =[]
        self.polygonActorList = []

        self.LenPickingPointsIm = []
        self.LenPickingPointVTK = []
        self.LenpolygonList =[]
        self.LenpolygonActorList = []

        self.setVtkVols()
        self.PresentCurser()

        # self.PresentPoint()

        if self.ViewMode == 'Axial':
            self.viewerLogic.AxialViewer = self
        elif self.ViewMode == 'Coronal':
            self.viewerLogic.CoronalViewer = self

        self.window.Render()

    def setVtkVols(self):
        if self.ViewMode == 'Axial':
            self.vtkVol = self.viewerLogic.AxialData
        elif self.ViewMode == 'Coronal':
            self.vtkVol = self.viewerLogic.CoronalData
        # self.vtkVol = self.viewerLogic.AxialData
        x0, y0, z0 = self.vtkVol.GetOrigin()
        x_spacing, y_spacing, z_spacing = self.vtkVol.GetSpacing()
        x_min, x_max, y_min, y_max, z_min, z_max = self.vtkVol.GetExtent()


        self.center = [x0 + x_spacing * 0.5 * (x_min + x_max),
                       y0 + y_spacing * 0.5 * (y_min + y_max),
                       z0 + z_spacing * 0.5 * (z_min + z_max)]

        self.StartCenter = self.center
        self.ZminVTK = z0
        self.ZmaxVTK = z0 + z_spacing * (z_min + z_max)
        # if (z_max-z_min+1)%2 == 0:
        #     self.ZminVTK = z0 - 0.5 * z_spacing
        #     self.ZmaxVTK = z0 + z_spacing * (z_max -z_min + 0.5)
        # else:
        #     self.ZminVTK = z0
        #     self.ZmaxVTK = z0 + z_spacing * (z_max -z_min + 1)

        # Matrices for axial, coronal, sagittal, oblique view orientations
        self.XY = vtk.vtkMatrix4x4()
        self.XY.DeepCopy((1, 0, 0, self.center[0],
                             0, -1, 0, self.center[1],
                             0, 0, 1, self.center[2],
                             0, 0, 0, 1))

        # self.axial = vtk.vtkMatrix4x4()
        #
        # self.axial.DeepCopy((1, 0, 0, self.center[0],
        #                      0, -1, 0, self.center[1],
        #                      0, 0, 1, self.center[2],
        #                      0, 0, 0, 1))
        #
        # self.coronal = vtk.vtkMatrix4x4()
        # self.coronal.DeepCopy((1, 0, 0, self.center[0],
        #                        0, 0, 1, self.center[1],
        #                        0, -1, 0, self.center[2],
        #                        0, 0, 0, 1))
        #
        # self.sagittal = vtk.vtkMatrix4x4()
        # self.sagittal.DeepCopy((0, 0, -1, self.center[0],
        #                         -1, 0, 0, self.center[1],
        #                         0, -1, 0, self.center[2],
        #                         0, 0, 0, 1))

        # Extract a slice in the desired orientation
        self.reslice = vtk.vtkImageReslice()
        self.reslice.SetInputData(self.vtkVol)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(self.XY)
        self.reslice.SetInterpolationModeToLinear()
        #self.reslice.SetOutputSpacing(x_spacing,x_spacing,x_spacing)
        self.reslice.Update()

        # Display the image
        self.actor = vtk.vtkImageActor()
        self.actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.actor.GetProperty().SetColorWindow(self.viewerLogic.WindowVal)
        self.actor.GetProperty().SetColorLevel(self.viewerLogic.LevelVal)


        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(171/255,216/255,1)
        self.renderer.AddActor(self.actor)

        self.window = self.interactor.GetRenderWindow()
        self.window.AddRenderer(self.renderer)

        self.interactorStyle = AxialViewerInteractorStyle.AxialViewerInteractorStyle(parent=self.interactor,
                                                                                     baseViewer=self)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.window.SetInteractor(self.interactor)

        # self.interactor.Initialize()
        # self.interactor.Start()

        extent = self.reslice.GetOutput().GetExtent()
        spacing = self.reslice.GetOutput().GetSpacing()
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()

        if self.ViewMode == 'Axial':
            self.renderer.GetActiveCamera().SetParallelScale(self.viewerLogic.AxialBaseParallelScale)
        elif self.ViewMode == 'Coronal':
            self.renderer.GetActiveCamera().SetParallelScale(self.viewerLogic.CoronalBaseParallelScale)

        self.textActorSliceIdx = vtk.vtkTextActor()
        self.textActorSliceIdx.GetTextProperty().SetFontSize(14)
        self.textActorSliceIdx.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorSliceIdx.SetDisplayPosition(0, 2)
        self.textActorSliceIdx.SetInput("SliceIdx: " + str(self.SliceIDx))
        self.renderer.AddActor(self.textActorSliceIdx)

        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: " + str(self.viewerLogic.WindowVal))
        self.renderer.AddActor(self.textActorWindow)

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: " + str(self.viewerLogic.LevelVal))
        self.renderer.AddActor(self.textActorLevel)
        self.window.Render()

    def UpdateViewerMatrixCenter(self, center, sliceIdx):
        matrix = self.reslice.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])

        self.textActorSliceIdx.SetInput("SliceIdx: " + str(sliceIdx))

        self.window.Render()
        self.center = center
        self.SliceIDx = sliceIdx
        if self.ViewMode == 'Axial':
            self.viewerLogic.AxialSliceID = sliceIdx
        elif self.ViewMode == 'Coronal':
            self.viewerLogic.CoronalSliceID = sliceIdx

        self.PresentPoint()

    def updateWindowLevel_Label(self):
        self.viewerLogic.WindowVal = self.actor.GetProperty().GetColorWindow()
        self.viewerLogic.LevelVal = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.viewerLogic.WindowVal)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.viewerLogic.LevelVal)))
        self.window.Render()

    def UpdateWindowLevel_Val(self):
        # self.actor.GetProperty().SetColorWindow(self.visualizationWindow)
        # self.actor.GetProperty().SetColorLevel(self.visualizationLevel)
        self.updateWindowLevel_Label()

    def AddToPickingList(self, PickingCoords):
        PointIdImage = np.zeros(3)
        # if self.ViewMode == 'Axial':
        #     spacing = self.viewerLogic.AxialVTKSpacing
        #     self.SliceIDx = self.viewerLogic.AxialSliceID
        #     picking_z = (self.SliceIDx - self.viewerLogic.AxialCenterSliceID)*spacing[2]
        #
        # elif self.ViewMode == 'Coronal':
        #     spacing = self.viewerLogic.CoronalVTKSpacing
        #     self.SliceIDx = self.viewerLogic.CoronalSliceID
        #     picking_z = (self.SliceIDx - self.viewerLogic.CoronalCenterSliceID) * spacing[2]
        # viewerOrigin = shape / 2.0
        # PointIdImage[2] = self.SliceIDx
        # PointIdImage[0] = PickingCoords[0] // spacing[0] + viewerOrigin[0]+1
        # #PointIdImage[1] = shape[1] - (PickingCoords[1] / spacing[1] + viewerOrigin[1])
        # PointIdImage[1] = viewerOrigin[1]-PickingCoords[1] // spacing[1]

        # PointIdImage = np.array([PickingCoords[0],PickingCoords[1],picking_z, self.SliceIDx]) #x,y,z,sliceID
        PointIdImage = np.array([PickingCoords[0], PickingCoords[1], PickingCoords[2], self.SliceIDx])  # x,y,z,sliceID
        # PointIdImage = np.int32(np.round(PointIdImage))
        # print("Points: " , PointIdImage)
        #
        PointIdImage = PointIdImage.tolist()
        print(PointIdImage)
        if PointIdImage in self.PickingPointsIm:
            print("need to remove point")
            i = self.PickingPointsIm.index(PointIdImage)
            actor = self.polygonActorList[i]
            self.renderer.RemoveActor(actor)
            self.window.Render()
            self.PickingPointsIm.remove(self.PickingPointsIm[i])
            self.PickingPointVTK.remove(self.PickingPointVTK[i])
            self.polygonList.remove(self.polygonList[i])
            self.polygonActorList.remove(self.polygonActorList[i])
        else:
            self.PickingPointsIm.append(PointIdImage)
            self.PickingPointVTK.append(PickingCoords)
            # print(self.PickingPointsIm)
            # print(self.PickingPointVTK)
            polygon = vtk.vtkRegularPolygonSource()
            DisplayCoord = (PickingCoords[0],PickingCoords[1],0)
            polygon.SetCenter(DisplayCoord)
            polygon.SetRadius(1)
            polygon.SetNumberOfSides(15)
            # polygon.SetNormal(1, 2, 3)
            polygon.GeneratePolylineOff()
            polygon.GeneratePolygonOn()
            polygonMapper = vtk.vtkPolyDataMapper()
            polygonMapper.SetInputConnection(polygon.GetOutputPort())
            polygonActor = vtk.vtkActor()
            polygonActor.SetMapper(polygonMapper)
            polygonActor.GetProperty().SetColor(1, 0, 0)
            polygonActor.GetProperty().SetAmbient(1)

            self.polygonActorList.append(polygonActor)
            self.polygonList.append(polygon)
            self.renderer.AddActor(polygonActor)

        self.PresentPoint()

    def AddToLenPickingList(self, PickingCoords):
        PointIdImage = np.zeros(3)
        # if self.ViewMode == 'Axial':
        #     spacing = self.viewerLogic.AxialVTKSpacing
        #     self.SliceIDx = self.viewerLogic.AxialSliceID
        #     picking_z = (self.SliceIDx - self.viewerLogic.AxialCenterSliceID)*spacing[2]
        #
        # elif self.ViewMode == 'Coronal':
        #     spacing = self.viewerLogic.CoronalVTKSpacing
        #     self.SliceIDx = self.viewerLogic.CoronalSliceID
        #     picking_z = (self.SliceIDx - self.viewerLogic.CoronalCenterSliceID) * spacing[2]

        # PointIdImage = np.array([PickingCoords[0],PickingCoords[1],picking_z, self.SliceIDx]) #x,y,z,sliceID
        PointIdImage = np.array([PickingCoords[0], PickingCoords[1], PickingCoords[2], self.SliceIDx])  # x,y,z,sliceID
        PointIdImage = PointIdImage.tolist()

        if PointIdImage in self.LenPickingPointsIm:
            print("need to remove point")
            i = self.PickingPointsIm.index(PointIdImage)
            actor = self.polygonActorList[i]
            self.renderer.RemoveActor(actor)
            self.window.Render()
            self.LenPickingPointsIm.remove(self.LenPickingPointsIm[i])
            self.LenPickingPointVTK.remove(self.LenPickingPointVTK[i])
            self.LenpolygonList.remove(self.LenpolygonList[i])
            self.LenpolygonActorList.remove(self.LenpolygonActorList[i])
        else:
            self.LenPickingPointsIm.append(PointIdImage)
            self.LenPickingPointVTK.append(PickingCoords)
            # print(self.PickingPointsIm)
            # print(self.PickingPointVTK)
            polygon = vtk.vtkRegularPolygonSource()
            DisplayCoord = (PickingCoords[0], PickingCoords[1], 0)
            polygon.SetCenter(DisplayCoord)
            polygon.SetRadius(1)
            polygon.SetNumberOfSides(15)
            # polygon.SetNormal(1, 2, 3)
            polygon.GeneratePolylineOff()
            polygon.GeneratePolygonOn()
            polygonMapper = vtk.vtkPolyDataMapper()
            polygonMapper.SetInputConnection(polygon.GetOutputPort())
            polygonActor = vtk.vtkActor()
            polygonActor.SetMapper(polygonMapper)
            polygonActor.GetProperty().SetColor(0, 1, 0)
            polygonActor.GetProperty().SetAmbient(1)

            self.LenpolygonActorList.append(polygonActor)
            self.LenpolygonList.append(polygon)
            self.renderer.AddActor(polygonActor)

        self.LenPresentPoint()

    def PresentPoint(self):
        for i in range(len(self.PickingPointsIm)):
            Point = self.PickingPointsIm[i]
            if Point[3] != self.SliceIDx:
                polygon = self.polygonList[i]
                polygon.GeneratePolygonOff()
            else:
                polygon = self.polygonList[i]
                polygon.GeneratePolygonOn()
            self.window.Render()

    def LenPresentPoint(self):
        for i in range(len(self.LenPickingPointsIm)):
            Point = self.LenPickingPointsIm[i]
            if Point[3] != self.SliceIDx:
                polygon = self.LenpolygonList[i]
                polygon.GeneratePolygonOff()
            else:
                polygon = self.LenpolygonList[i]
                polygon.GeneratePolygonOn()
            self.window.Render()

    def PresentCurser(self):
        start_idx_image = np.zeros(3)
        if self.ViewMode == 'Axial':
            spacing = self.viewerLogic.AxialVTKSpacing
            shape = np.asarray(self.viewerLogic.AxialDimensions)
        elif self.ViewMode == 'Coronal':
            spacing = self.viewerLogic.CoronalVTKSpacing
            shape = np.asarray(self.viewerLogic.CoronalDimensions)

        extent = self.reslice.GetOutput().GetExtent()

        start_idx_image[2] = self.SliceIDx
        start_idx_image[0] = 0
        start_idx_image[1] = 0
        start_idx_image = np.int32(np.round(start_idx_image))

        self.Cursor = vtk.vtkCursor2D()
        xmin = start_idx_image[0]-0.5 * ((extent[1] - extent[0]) * spacing[0])
        xmax =start_idx_image[0]+ 0.5 * ((extent[1] - extent[0]) * spacing[0])
        ymin = start_idx_image[1]-0.5 * ((extent[3] - extent[2]) * spacing[1])
        ymax = start_idx_image[1]+ 0.5 * ((extent[3] - extent[2]) * spacing[1])
        # zmin = start_idx_image[2]-0.5 * ((extent[5] - extent[4]) * spacing[2])
        # zmax = start_idx_image[2]+ 0.5 * ((extent[5] - extent[4]) * spacing[2])
        self.Cursor.SetModelBounds(-10000,10000,-10000,10000,0,0)

        self.Cursor.SetFocalPoint(0, 0, 0)
        # self.Cursor.AllOff()
        self.Cursor.AxesOn()
        self.Cursor.TranslationModeOn()
        self.Cursor.OutlineOff()
        cursorMapperAx = vtk.vtkPolyDataMapper()
        cursorMapperAx.SetInputConnection(self.Cursor.GetOutputPort())
        cursorActorAx = vtk.vtkActor()
        cursorActorAx.SetMapper(cursorMapperAx)
        cursorActorAx.GetProperty().SetColor(1, 0, 0)
        self.renderer.AddActor(cursorActorAx)
        # self.window.Render()
        # print("Cursor bounds: ", self.Cursor.GetModelBounds())

    def Start(self):

        # Start interaction
        self.interactor.Initialize()
        self.interactor.Start()
    '''
    def MoveCursor(self, PkinigCurserCoords):
        PointIdImage = np.zeros(3)
        if self.ViewMode == 'Axial':
            spacing = self.viewerLogic.AxialVTKspacing
            shape = np.asarray(self.viewerLogic.AxialDimensions)
            self.SliceIDx = self.viewerLogic.AxialSliceID
        elif self.ViewMode == 'Coronal':
            spacing = self.viewerLogic.CoronalVTKspacing
            shape = np.asarray(self.viewerLogic.CoronalDimensions)
            self.SliceIDx = self.viewerLogic.CoronalSliceID
        viewerOrigin = shape / 2.0
        PointIdImage[2] = self.SliceIDx
        PointIdImage[0] = PkinigCurserCoords[0] / spacing[0]  + viewerOrigin[0]
        PointIdImage[1] = shape[1] - (PkinigCurserCoords[1] / spacing[1]  + viewerOrigin[1])
        #PointIdImage[1] = shape[1] - (PkinigCurserCoords[1] / spacing[1])#  + viewerOrigin[1]
        PointIdImage = np.int32(np.round(PointIdImage))
        print(self.viewerLogic.AxialDimensions)
        print(PointIdImage)
        print(PkinigCurserCoords)
        self.Cursor.SetFocalPoint(PkinigCurserCoords)
        self.window.Render()
    '''
