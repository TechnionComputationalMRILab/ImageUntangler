from vtkmodules.all import vtkInteractorStyleImage, vtkPointPicker
import numpy as np

import logging
logging.getLogger(__name__)


class MPRInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, parent, MPRWindow, model):
        super().__init__()

        self.model = model
        self.MPRWindow = MPRWindow
        self.parent = parent
        self.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        self.AddObserver("MiddleButtonPressEvent", self.ButtonCallback)
        self.AddObserver("MiddleButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonPressEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("RightButtonPressEvent", self.ButtonCallback)
        self.AddObserver("RightButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("MouseWheelForwardEvent", self.MouseWheelForwardCallback)
        self.AddObserver("MouseWheelBackwardEvent", self.MouseWheelBackwardCallback)

        self.actions = {"Rotating": 0,
                        "Windowing": 0,
                        "Zooming": 0,
                        "Panning": 0,
                        "Picking": 0}  # Create callbacks for slicing the image

        self.picker = vtkPointPicker()

    def MouseWheelForwardCallback(self, obj, event):
        self.MPRWindow.update_angle(1)

    def MouseWheelBackwardCallback(self, obj, event):
        self.MPRWindow.update_angle(-1)

    def ButtonCallback(self, obj, event):
        Shift = self.parent.GetShiftKey()
        if event == "MiddleButtonPressEvent":
            if Shift ==1:
                self.actions["Panning"] = 1
                vtkInteractorStyleImage.OnMiddleButtonDown(self)
            else:
                self.actions["Rotating"] = 1
        elif event == "MiddleButtonReleaseEvent":
            if Shift == 1:
                self.actions["Panning"] = 0
                vtkInteractorStyleImage.OnMiddleButtonUp(self)
            else:
                self.actions["Rotating"] = 0

        if event == "LeftButtonPressEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["Picking"] == 1:
                self.OnPickingLeftButtonDown()
            else:
                self.actions["Windowing"] = 1
                vtkInteractorStyleImage.OnLeftButtonDown(self)

        elif event == "LeftButtonReleaseEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["Picking"] == 0:
                self.actions["Windowing"] = 0
                vtkInteractorStyleImage.OnLeftButtonUp(self)
            else:
                self.OnPickingLeftButtonUp(mouseX, mouseY)

        if event == "RightButtonPressEvent":
            self.actions["Zooming"] = 1
            vtkInteractorStyleImage.OnRightButtonDown(self)

        elif event == "RightButtonReleaseEvent":
            self.actions["Zooming"] = 0
            vtkInteractorStyleImage.OnRightButtonUp(self)

    def MouseMoveCallback(self, obj, event):
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()
        center = self.MPRWindow.renderWindow.GetSize()
        centerX = center[0] / 2.0
        centerY = center[1] / 2.0

        if self.actions["Rotating"] == 1:
            screenSize = self.parent.GetRenderWindow().GetSize()
            angle = np.int32(np.round(180.0 * mouseY / screenSize[1]))
            self.MPRWindow.changeAngle(angle)

        elif self.actions["Windowing"] == 1:

            vtkInteractorStyleImage.OnMouseMove(self)
            self.MPRWindow.updateWindowAndLevel()

        elif self.actions["Zooming"] == 1:
            self.Dolly(self.MPRWindow.renderer, self.MPRWindow.renderer.GetActiveCamera(), mouseX, mouseY, lastX, lastY,
                  centerX, centerY)

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
