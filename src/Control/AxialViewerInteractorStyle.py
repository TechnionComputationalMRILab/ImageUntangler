from vtk import vtkInteractorStyleImage, vtkPropPicker


class AxialViewerInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, parent, interface):
        self.interface = interface
        self.parent = parent
        self.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        self.AddObserver("MiddleButtonPressEvent", self.ButtonCallback)
        self.AddObserver("MiddleButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonPressEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("RightButtonPressEvent", self.ButtonCallback)
        self.AddObserver("RightButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("KeyPressEvent", self.KeyPressCallback)
        self.AddObserver("MouseWheelForwardEvent", self.MouseWheelCallback)
        self.AddObserver("MouseWheelBackwardEvent", self.MouseWheelCallback)


        ## Create callbacks for slicing the image
        self.actions = dict()
        self.actions["Slicing"] = 0
        self.actions["Windowing"] = 0
        self.actions["Zooming"] = 0
        self.actions["PickingMPR"] = 0
        self.actions["PickingLength"] = 0
        self.actions["Cursor"] = 0
        self.actions["Panning"] = 0

        self.pointPicker = vtkPropPicker()

        self.startPickingEvent = False
        self.ShowCursor = True

    def ButtonCallback(self, obj, event):
        Shift = self.parent.GetShiftKey()
        if event == "MiddleButtonPressEvent":
            if self.parent.GetShiftKey() == 1:
                self.actions["Panning"] = 1
                vtkInteractorStyleImage.OnMiddleButtonDown(self)
            else:
                self.actions["Slicing"] = 1

        elif event == "MiddleButtonReleaseEvent":
            if Shift == 1:
                self.actions["Panning"] = 0
                vtkInteractorStyleImage.OnMiddleButtonUp(self)
            else:
                self.actions["Slicing"] = 0

        if event == "RightButtonPressEvent":
            self.actions["Zooming"] = 1
            vtkInteractorStyleImage.OnRightButtonDown(self)

        elif event == "RightButtonReleaseEvent":
            self.actions["Zooming"] = 0
            vtkInteractorStyleImage.OnRightButtonUp(self)

        if event == "LeftButtonPressEvent":
            self.actions["Cursor"] = self.cursorInBullsEye()
            if self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 0:
                self.actions["Windowing"] = 1
                vtkInteractorStyleImage.OnLeftButtonDown(self)
            elif self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 1:
                AxialViewerInteractorStyle.OnPickingCurserLeftButtonDown(self)
            elif self.actions["PickingMPR"] == 1:
                AxialViewerInteractorStyle.OnPickingLeftButtonDown(self)
            elif self.actions["PickingLength"] == 1:
                AxialViewerInteractorStyle.OnPickingLeftButtonDown(self)

        elif event == "LeftButtonReleaseEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 0:
                self.actions["Windowing"] = 0
                vtkInteractorStyleImage.OnLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 1:
                self.actions["Cursor"] = 0
                AxialViewerInteractorStyle.OnPickingCursorLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 1:
                AxialViewerInteractorStyle.pickPoint(self, "MPRwindow", mouseX, mouseY)
            elif self.actions["PickingLength"] == 1:
                AxialViewerInteractorStyle.pickPoint(self, "Length", mouseX, mouseY)

    def MouseMoveCallback(self, obj, event):
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()

        if self.actions["Slicing"] == 1:
            deltaY = mouseY - lastY
            self.interface.changeSliceIndex(deltaY)

        elif self.actions["Windowing"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            self.interface.updateWindowLevel()

        elif self.actions["Zooming"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            self.interface.updateZoomFactor()
        else:
            self.OnMouseMove() # call to superclass

    def KeyPressCallback(self, obj, event):
        if self.parent.GetKeyCode() == 'C' or self.parent.GetKeyCode() == 'c':
            if self.ShowCursor:
                self.ShowCursor = False
                self.interface.clearCursor()

            else:
                self.ShowCursor = True
                self.interface.addCursor()

        elif self.parent.GetKeySym() == 'Up':
            self.interface.changeSliceIndex(increment=True)

        elif self.parent.GetKeySym() == 'Down':
            self.interface.changeSliceIndex(increment=False)

    def cursorInBullsEye(self) -> int:
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.interface.view.renderer): #REMOVE
            StartCursorPickedCoordinates = self.pointPicker.GetPickPosition()
            cursorFocalPoint = self.interface.view.Cursor.GetFocalPoint()
            if (abs(StartCursorPickedCoordinates[0]-cursorFocalPoint[0]) <= 3*self.interface.view.Cursor.GetRadius())\
                    and (abs(StartCursorPickedCoordinates[1]-cursorFocalPoint[1]) <= self.interface.view.Cursor.GetRadius()):
                return 1
            else:
                return 0


    def pickPoint(self, pointType: str, mouseX, mouseY):
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.interface.view.renderer):
            pickedCoordinates = self.pointPicker.GetPickPosition()
            matrix = self.interface.view.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            zCoordinate = (center[2] - self.interface.view.imageData.origin[2]) - self.interface.view.imageData.dimensions[2]\
                             * self.interface.view.imageData.spacing[2] / 2
            pickedCoordinates = (pickedCoordinates[0], pickedCoordinates[1], zCoordinate)

            self.interface.view.addPoint(pointType, pickedCoordinates)

    def OnPickingCursorLeftButtonUp(self):
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.interface.view.renderer):
            cursorPickedCoordinates = self.pointPicker.GetPickPosition()
            self.interface.moveBullsEye(cursorPickedCoordinates)

    def OnPickingCurserLeftButtonDown(self):
        pass

    def MouseWheelCallback(self, obj,event):
        pass

    def OnPickingLeftButtonDown(self):
        pass



