import vtkmodules.all as vtk
import numpy as np


class MPRInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, parent, MPRWindow):
        super().__init__()

        self.MPRWindow = MPRWindow
        self.parent = parent
        self.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        self.AddObserver("MiddleButtonPressEvent", self.ButtonCallback)
        self.AddObserver("MiddleButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonPressEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("RightButtonPressEvent", self.ButtonCallback)
        self.AddObserver("RightButtonReleaseEvent", self.ButtonCallback)

        ## Create callbacks for slicing the image
        self.actions = {}
        self.actions["Rotating"] = 0
        self.actions["Windowing"] = 0
        self.actions["Zooming"] = 0
        self.actions["Panning"] = 0
        self.actions["Picking"] = 0

        self.picker = vtk.vtkPointPicker()

    def ButtonCallback(self, obj, event):
        Shift = self.parent.GetShiftKey()
        if event == "MiddleButtonPressEvent":
            if Shift ==1:
                self.actions["Panning"] = 1
                vtk.vtkInteractorStyleImage.OnMiddleButtonDown(self)
            else:
                self.actions["Rotating"] = 1
        elif event == "MiddleButtonReleaseEvent":
            if Shift == 1:
                self.actions["Panning"] = 0
                vtk.vtkInteractorStyleImage.OnMiddleButtonUp(self)
            else:
                self.actions["Rotating"] = 0

        if event == "LeftButtonPressEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["Picking"] == 1:
                self.OnPickingLeftButtonDown()
            else:
                self.actions["Windowing"] = 1
                vtk.vtkInteractorStyleImage.OnLeftButtonDown(self)

        elif event == "LeftButtonReleaseEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["Picking"] == 0:
                self.actions["Windowing"] = 0
                vtk.vtkInteractorStyleImage.OnLeftButtonUp(self)
            else:
                self.OnPickingLeftButtonUp(mouseX, mouseY)

        if event == "RightButtonPressEvent":
            self.actions["Zooming"] = 1
            vtk.vtkInteractorStyleImage.OnRightButtonDown(self)

        elif event == "RightButtonReleaseEvent":
            self.actions["Zooming"] = 0
            vtk.vtkInteractorStyleImage.OnRightButtonUp(self)


    def MouseMoveCallback(self, obj, event):
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()
        center = self.MPRWindow.renderWindow.GetSize()
        centerX = center[0] / 2.0
        centerY = center[1] / 2.0

        if self.actions["Rotating"] == 1:
            screenSize = self.parent.GetRenderWindow().GetSize()
            angle = np.int32(np.round(180.0 * mouseY / screenSize[1]))
            # print(angle)
            self.MPRWindow.changeAngle(angle)
            # self.MPRWindow.Angle.setValue(angle)
            # self.baseViewer.generateSMPR(viewAngle=angle)
            # self.baseViewer.updateSMPRVisualization()
            # self.baseViewer.window.Render()
        #
        elif self.actions["Windowing"] == 1:

            vtk.vtkInteractorStyleImage.OnMouseMove(self)
            self.MPRWindow.updateWindowAndLevel()

        #
        elif self.actions["Zooming"] == 1:
            self.Dolly(self.MPRWindow.renderer, self.MPRWindow.renderer.GetActiveCamera(), mouseX, mouseY, lastX, lastY,
                  centerX, centerY)
        #     vtk.vtkInteractorStyleImage.OnMouseMove(self)
        #     curParallelScale = self.baseViewer.renderer.GetActiveCamera().GetParallelScale()
        #     zoomFactor = curParallelScale / self.baseViewer.baseParallelScale
        #     self.baseViewer.cardiacViewerLogic.updateZoomFacotr(zoomFactor, 'smpr')

        # elif self.actions["Panning"] == 1:

        else:
            self.OnMouseMove()

    def Dolly(self, renderer, camera, x, y, lastX, lastY, centerX, centerY):
        dollyFactor = pow(1.02, (0.5 * (y - lastY)))
        if camera.GetParallelProjection():
            parallelScale = camera.GetParallelScale() * dollyFactor
            camera.SetParallelScale(parallelScale)
        else:
            camera.Dolly(dollyFactor)
            renderer.ResetCameraClippingRange()

        self.MPRWindow.renderWindow.Render()

    def OnPickingLeftButtonDown(self):
        pass

    def OnPickingLeftButtonUp(self,mouseX,mouseY):
        if self.picker.Pick(mouseX, mouseY, 0.0, self.MPRWindow.renderer):
            pickedCoordinates = self.picker.GetPickPosition()
            self.MPRWindow.processNewPoint(pickedCoordinates)



