import vtk
import MPRInteractor
import numpy as np
from vtk.util import numpy_support
import getMPR
import MPRWindow

class View():

    # ZminVTK: object

    def __init__(self, interactor,MPRViewerProperties):
        self.interactor = interactor
        self.MPRViewerProperties = MPRViewerProperties
        self.PickingPointsIm = []
        self.polygonList = []
        self.polygonActorList = []
        self.PickingPointsIndex =[]
        self.Visualize_MPR()

    def Visualize_MPR(self):
        MPR_M = self.MPRViewerProperties.MPR_M
        delta = self.MPRViewerProperties.delta
        n = MPR_M.shape[0]
        m = MPR_M.shape[1]
        MPR_vtk = vtk.vtkImageData()
        MPR_vtk.SetDimensions(n, m,1)
        origin=[0,0,0]
        MPR_vtk.SetOrigin(origin)
        # MPR_vtk.SetSpacing([1,1,1])
        MPR_vtk.SetSpacing([delta,delta,delta])
        # MPR_vtk.SetExtent(0, MPR_M.shape[1] - 1, 0, MPR_M.shape[0] - 1, 0, 0)
        # nPoints = plane.GetOutput().GetNumberOfPoints()
        # assert (nPoints == MPR_M.size)
        #
        vtk_type_by_numpy_type = {
            np.uint8: vtk.VTK_UNSIGNED_CHAR,
            np.uint16: vtk.VTK_UNSIGNED_SHORT,
            np.uint32: vtk.VTK_UNSIGNED_INT,
            np.uint64: vtk.VTK_UNSIGNED_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_UNSIGNED_LONG_LONG,
            np.int8: vtk.VTK_CHAR,
            np.int16: vtk.VTK_SHORT,
            np.int32: vtk.VTK_INT,
            np.int64: vtk.VTK_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_LONG_LONG,
            np.float32: vtk.VTK_FLOAT,
            np.float64: vtk.VTK_DOUBLE
        }
        vtk_datatype = vtk_type_by_numpy_type[MPR_M.dtype.type]
        MPR_M = np.transpose(MPR_M)
        scalars = numpy_support.numpy_to_vtk(num_array=MPR_M.ravel(), deep=True, array_type=vtk_datatype)

        MPR_vtk.GetPointData().SetScalars(scalars)
        MPR_vtk.Modified()
        self.actor = vtk.vtkImageActor()
        self.actor.GetMapper().SetInputData(MPR_vtk)


        #Renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(171/255,216/255,1)
        self.renderer.ResetCamera()

        # self.interactor = QVTKRenderWindowInteractor(self.groupBox)
        # self.gridLayout.addWidget(self.interactor, 0, 0, 1, 3)
        self.renderWindow = self.interactor.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractor.MPRInteractorStyle(parent=self.interactor, MPRWindow=self)
        self.interactorStyle.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.renderWindow.SetInteractor(self.interactor)


        #renderWindowInteractor = vtk.vtkRenderWindowInteractor()

        self.renderWindow.SetInteractor(self.interactor)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCamera()
        self.interactor.Initialize()
        #interactor.Start()

        # self.MPRViewerProperties.window = self.actor.GetProperty().GetColorWindow()
        # self.MPRViewerProperties.level = self.actor.GetProperty().GetColorLevel()

        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(14)
        self.textActorWindow.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorWindow.SetDisplayPosition(0, 17)
        self.textActorWindow.SetInput("Window: " + str(self.MPRViewerProperties.window))
        self.renderer.AddActor(self.textActorWindow)

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(14)
        self.textActorLevel.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorLevel.SetDisplayPosition(0, 32)
        self.textActorLevel.SetInput("Level: " + str(self.MPRViewerProperties.level))
        self.renderer.AddActor(self.textActorLevel)

        self.textActorAngle = vtk.vtkTextActor()
        self.textActorAngle.GetTextProperty().SetFontSize(14)
        self.textActorAngle.GetTextProperty().SetColor(51/255, 51/255, 1)
        self.textActorAngle.SetDisplayPosition(0, 47)
        self.textActorAngle.SetInput("Angle: " + str(self.MPRViewerProperties.angle))
        self.renderer.AddActor(self.textActorAngle)


        self.renderWindow.Render()
        # self.interactor.Start()

    def window_label_update(self):
        self.MPRViewerProperties.window = self.actor.GetProperty().GetColorWindow()
        self.MPRViewerProperties.level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(self.MPRViewerProperties.window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(self.MPRViewerProperties.level)))
        self.textActorAngle.SetInput("Angle: " + str(np.int32(self.MPRViewerProperties.angle)))
        self.renderWindow.Render()

    def AngleChangeByIneractor(self,angle):
        Height = self.MPRViewerProperties.Height
        self.MPRViewerProperties.angle = angle
        plot = 0
        GetMPR = getMPR.PointsToPlansVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.ListOfPoints_Original,
                                             self.MPRViewerProperties.ConvViewMode, Height=Height,


                                             viewAngle=angle, Plot=plot)
        self.MPRViewerProperties.MPR_M = GetMPR.MPR_M
        self.MPRViewerProperties.delta = GetMPR.delta
        self.MPRViewerProperties.MPRPosiotion = GetMPR.MPR_indexs_np

        # MPRWindow.Ui_MPRWindow.spinBox.setValue(angle)

        self.Visualize_MPR()
        self.window_label_update()

    def AddToPickingList(self, PickingCoords):
        picking_z = 0
        PointIdImage = np.array([PickingCoords[0],PickingCoords[1],picking_z]) #x,y,z,sliceID
        PointIdImage = PointIdImage.tolist()

        # extent_x = self.MPRViewerProperties.MPR_M.shape[0]*self.MPRViewerProperties.delta
        # extent_y = self.MPRViewerProperties.MPR_M.shape[1]*self.MPRViewerProperties.delta
        print(self.MPRViewerProperties.MPR_M.shape)
        x_pixel = np.int(PickingCoords[0]//self.MPRViewerProperties.delta)
        y_pixel = np.int(PickingCoords[1]//self.MPRViewerProperties.delta)
        PointsIndex =  [x_pixel,y_pixel]
        # PointIdImage_Pixel = %[0,0] - left, bottom corner
        if PointIdImage in self.PickingPointsIm:
            print("need to remove point")
            i = self.PickingPointsIm.index(PointIdImage)
            actor = self.polygonActorList[i]
            self.renderer.RemoveActor(actor)
            self.renderWindow.Render()
            self.PickingPointsIm.remove(self.PickingPointsIm[i])
            self.PickingPointsIndex.remove(self.PickingPointsIndex[i])
            self.polygonList.remove(self.polygonList[i])
            self.polygonActorList.remove(self.polygonActorList[i])
        else:
            self.PickingPointsIm.append(PointIdImage)
            self.PickingPointsIndex.append(PointsIndex)
            print(self.PickingPointsIm)
            print(self.PickingPointsIndex)
            # print(self.PickingPointVTK)
            polygon = vtk.vtkRegularPolygonSource()
            polygon.SetCenter(PickingCoords)
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

    def PresentPoint(self):
        for i in range(len(self.PickingPointsIm)):
            polygon = self.polygonList[i]
            polygon.GeneratePolygonOn()
            self.renderWindow.Render()