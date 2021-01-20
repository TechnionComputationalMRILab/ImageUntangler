from icecream import ic
from vtk import vtkInteractorStyleImage, vtkPropPicker, vtkCellPicker, vtkMatrix4x4


class AxialViewerInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, parent, baseViewer, viewMode: str):
        self.baseViewer = baseViewer
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

        self.viewMode = viewMode
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
                AxialViewerInteractorStyle.pickPoint(self, "MPR", mouseX, mouseY)
            elif self.actions["PickingLength"] == 1:
                AxialViewerInteractorStyle.pickPoint(self, "Length", mouseX, mouseY)

    def adjustSliceIdx(self, transformZ: int):
        """ adjusts the slice of the MRI that is being viewed"""
        matrix: vtkMatrix4x4 = self.baseViewer.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, transformZ, 1))
        sliceIdx = int((center[2] - self.baseViewer.imageData.origin[2]) /
                       self.baseViewer.imageData.spacing[2] - 0.5)  # z - z_orig/(z_spacing - .5). slice idx is z coordinate of slice of image
        if 0 <= sliceIdx <= self.baseViewer.imageData.extent[5]:
            self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

    def MouseMoveCallback(self, obj, event):
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()

        if self.actions["Slicing"] == 1:
            deltaY = mouseY - lastY
            self.baseViewer.reslice.Update()
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            self.adjustSliceIdx(sliceSpacing * deltaY)

        elif self.actions["Windowing"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            self.baseViewer.updateWindowAndLevel()

        elif self.actions["Zooming"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            curParallelScale = self.baseViewer.renderer.GetActiveCamera().GetParallelScale()
            zoomFactor = curParallelScale / self.baseViewer.imageData.getParallelScale()
            self.baseViewer.viewerLogic.updateZoomFactor(zoomFactor)
        else:
            self.OnMouseMove() # call to superclass

    def KeyPressCallback(self, obj, event):
        if self.parent.GetKeyCode() == 'C' or self.parent.GetKeyCode() == 'c':
            if self.ShowCursor:
                self.ShowCursor = False
                self.baseViewer.Cursor.AllOff()
                self.baseViewer.window.Render()
            else:
                self.ShowCursor = True
                self.baseViewer.Cursor.AllOff()
                self.baseViewer.Cursor.AxesOn()
                self.baseViewer.window.Render()

        elif self.parent.GetKeySym() == 'Up':
            self.baseViewer.reslice.Update()
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            self.adjustSliceIdx(sliceSpacing)

        elif self.parent.GetKeySym() == 'Down':
            self.baseViewer.reslice.Update()
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            self.adjustSliceIdx(-1*sliceSpacing)

    def pickPoint(self, pointType: str, mouseX, mouseY):
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            pickedCoordinates = self.pointPicker.GetPickPosition()
            matrix = self.baseViewer.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            zCoordinate = (center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) - self.baseViewer.viewerLogic.CoronalData.dimensions[2]\
                             * self.baseViewer.viewerLogic.CoronalData.spacing[2] / 2
            pickedCoordinates = (pickedCoordinates[0], pickedCoordinates[1], zCoordinate)
            self.pickedCoordinates = pickedCoordinates
            self.baseViewer.addPoint(pointType, self.pickedCoordinates)

    def cursorInBullsEye(self) -> int:
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            StartCursorPickedCoordinates = self.pointPicker.GetPickPosition()
            cursorFocalPoint = self.baseViewer.Cursor.GetFocalPoint()
            if (abs(StartCursorPickedCoordinates[0]-cursorFocalPoint[0]) <= 3*self.baseViewer.Cursor.GetRadius())\
                    and (abs(StartCursorPickedCoordinates[1]-cursorFocalPoint[1]) <= self.baseViewer.Cursor.GetRadius()):
                return 1
            else:
                return 0

    def OnPickingCursorLeftButtonUp(self):
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            cursorPickedCoordinates = self.pointPicker.GetPickPosition()
            self.baseViewer.viewerLogic.moveBullsEye(cursorPickedCoordinates, self.viewMode)

    def OnPickingCurserLeftButtonDown(self):
        pass

    def MouseWheelCallback(self, obj,event):
        pass

    def OnPickingLeftButtonDown(self):
        pass



