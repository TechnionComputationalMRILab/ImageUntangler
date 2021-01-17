import vtk


class AxialViewerInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, parent, baseViewer):
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

        self.picker = vtk.vtkPropPicker()
        self.picker2 = vtk.vtkCellPicker()
        # self.picker = vtk.vtkPointPicker()
        # self.PickingCoordslist = []
        self.viewMode = self.baseViewer.ViewMode
        self.startPickingEvent = False
        self.ShowCursor = True

    def ButtonCallback(self, obj, event):
        Shift = self.parent.GetShiftKey()
        if event == "MiddleButtonPressEvent":
            if self.parent.GetShiftKey() == 1:
                self.actions["Panning"] = 1
                vtk.vtkInteractorStyleImage.OnMiddleButtonDown(self)
            else:
                self.actions["Slicing"] = 1

        elif event == "MiddleButtonReleaseEvent":
            if Shift == 1:
                self.actions["Panning"] = 0
                vtk.vtkInteractorStyleImage.OnMiddleButtonUp(self)
            else:
                self.actions["Slicing"] = 0

        if event == "RightButtonPressEvent":
            self.actions["Zooming"] = 1
            vtk.vtkInteractorStyleImage.OnRightButtonDown(self)

        elif event == "RightButtonReleaseEvent":
            self.actions["Zooming"] = 0
            vtk.vtkInteractorStyleImage.OnRightButtonUp(self)

        if event == "LeftButtonPressEvent":
            self.CursorStatus()
            if self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 0:
                self.actions["Windowing"] = 1
                vtk.vtkInteractorStyleImage.OnLeftButtonDown(self)
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
                vtk.vtkInteractorStyleImage.OnLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 1:
                self.actions["Cursor"] = 0
                AxialViewerInteractorStyle.OnPickingCursorLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 1:
                AxialViewerInteractorStyle.OnPickingLeftButtonUp(self,mouseX,mouseY)
            elif self.actions["PickingLength"] == 1:
                AxialViewerInteractorStyle.OnPickingLeftButtonUpLength(self,mouseX,mouseY)

    def MouseMoveCallback(self, obj, event):
        # print(self.parent.GetEventPosition())
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()

        if self.actions["Slicing"] == 1:

            deltaY = mouseY - lastY
            self.baseViewer.reslice.Update()
            matrix = self.baseViewer.reslice.GetResliceAxes()

            # move the center point that we are slicing through
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            # center_z = matrix.GetElement(2, 3) + sliceSpacing* deltaY
            # center = (matrix.GetElement(0, 3), matrix.GetElement(1, 3), center_z, 1)
            center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
            if self.viewMode == 'Axial':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.AxialVTKOrigin[2]) /
                #                      self.baseViewer.viewerLogic.AxialVTKSpacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.spacing[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

            elif self.viewMode == 'Coronal':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                #                      self.baseViewer.viewerLogic.CoronalData.spacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.spacing[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

            # self.baseViewer.PresentPoint()


        elif self.actions["Windowing"] == 1:
            vtk.vtkInteractorStyleImage.OnMouseMove(self)
            self.baseViewer.updateWindowLevel_Label()

        elif self.actions["Zooming"] == 1:
            vtk.vtkInteractorStyleImage.OnMouseMove(self)
            curParallelScale = self.baseViewer.renderer.GetActiveCamera().GetParallelScale()
            if self.viewMode == 'Axial':
                zoomFactor = curParallelScale / self.baseViewer.viewerLogic.AxialBaseParallelScale
            elif self.viewMode == 'Coronal':
                zoomFactor = curParallelScale / self.baseViewer.viewerLogic.CoronalBaseParallelScale
            self.baseViewer.viewerLogic.updateZoomFactor(zoomFactor)
        else:
            self.OnMouseMove()

    def KeyPressCallback(self, obj, event):
        if self.parent.GetKeyCode() == 'C' or self.parent.GetKeyCode() == 'c':
            if self.ShowCursor == False:
                self.ShowCursor = True
                self.baseViewer.Cursor.AllOff()
                self.baseViewer.Cursor.AxesOn()
                self.baseViewer.window.Render()

            elif self.ShowCursor == True:
                self.ShowCursor = False
                self.baseViewer.Cursor.AllOff()
                self.baseViewer.window.Render()

        if self.parent.GetKeySym() == 'Up':
            self.baseViewer.reslice.Update()
            matrix = self.baseViewer.reslice.GetResliceAxes()

            # move the center point that we are slicing through
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            # center_z = matrix.GetElement(2, 3) + sliceSpacing
            # center = (matrix.GetElement(0, 3), matrix.GetElement(1, 3), center_z, 1)
            center = matrix.MultiplyPoint((0, 0, sliceSpacing , 1))
            if self.viewMode == 'Axial':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.AxialVTKOrigin[2]) /
                #                      self.baseViewer.viewerLogic.AxialVTKSpacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.spacing[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

            elif self.viewMode == 'Coronal':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                #                      self.baseViewer.viewerLogic.CoronalData.spacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.spacing[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

            # if self.viewMode == 'Axial':
            #     sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.AxialVTKOrigin[2])/
            #                    self.baseViewer.viewerLogic.AxialVTKSpacing[2] + 0.5))
            #     if sliceIdx>= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
            #         self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)
            #
            # elif self.viewMode == 'Coronal':
            #     sliceIdx =int(round((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
            #                    self.baseViewer.viewerLogic.CoronalData.spacing[2] + 0.5))
            #     if sliceIdx>= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
            #         self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)
            # self.baseViewer.PresentPoint()

        if self.parent.GetKeySym() == 'Down':
            self.baseViewer.reslice.Update()
            matrix = self.baseViewer.reslice.GetResliceAxes()

            # move the center point that we are slicing through
            sliceSpacing = self.baseViewer.reslice.GetOutput().GetSpacing()[2]
            # center_z = matrix.GetElement(2, 3) - sliceSpacing
            # center = (matrix.GetElement(0, 3), matrix.GetElement(1, 3), center_z, 1)
            center = matrix.MultiplyPoint((0, 0, -1*sliceSpacing, 1))
            if self.viewMode == 'Axial':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.AxialVTKOrigin[2]) /
                #                      self.baseViewer.viewerLogic.AxialVTKSpacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.extent[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)

            elif self.viewMode == 'Coronal':
                # sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                #                      self.baseViewer.viewerLogic.CoronalData.spacing[2] + 0.5))
                sliceIdx = int((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
                               self.baseViewer.viewerLogic.CoronalData.spacing[2] - 0.5)
                if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
                    self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)
            # if self.viewMode == 'Axial':
            #     sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.AxialVTKOrigin[2])
            #                     / self.baseViewer.viewerLogic.AxialVTKSpacing[2] + 0.5))
            #     # if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
            #     if sliceIdx>= 0 and sliceIdx <= self.baseViewer.viewerLogic.AxialData.extent[5]:
            #         self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)
            #
            # elif self.viewMode == 'Coronal':
            #     sliceIdx = int(round((center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) /
            #                    self.baseViewer.viewerLogic.CoronalData.spacing[2] + 0.5))
            #     if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
            #         # if sliceIdx >= 0 and sliceIdx <= self.baseViewer.viewerLogic.CoronalData.extent[5]:
            #         self.baseViewer.UpdateViewerMatrixCenter(center, sliceIdx)
            # self.baseViewer.PresentPoint()

    def MouseWheelCallback(self, obj,event):
        pass

    def OnPickingLeftButtonDown(self):
        pass
    
    def OnPickingLeftButtonUp(self, mouseX, mouseY):
        # print((mouseX, mouseY))
        if self.picker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            self.picker2.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer)
            print(self.picker2.GetPointIJK())
            PickingCoords = self.picker.GetPickPosition()
            matrix = self.baseViewer.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            # PickingCoordsZ = center[2]-self.baseViewer.viewerLogic.start_center_z
            # PickingCoordsZ = (center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2])
            PickingCoordsZ = (center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) - self.baseViewer.viewerLogic.CoronalData.dimensions[2]\
                             * self.baseViewer.viewerLogic.CoronalData.spacing[2] / 2
            PickingCoords = (PickingCoords[0],PickingCoords[1],PickingCoordsZ)
            # PickingCoordsold = self.pickerold.GetPickPosition()
            self.PickingCoords = PickingCoords
            self.baseViewer.AddToPickingList(self.PickingCoords)

    def OnPickingLeftButtonUpLength(self,mouseX,mouseY):
        # print((mouseX, mouseY))

        if self.picker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            PickingCoords = self.picker.GetPickPosition()
            matrix = self.baseViewer.reslice.GetResliceAxes()
            center = matrix.MultiplyPoint((0, 0, 0, 1))
            PickingCoordsZ = (center[2] - self.baseViewer.viewerLogic.CoronalData.origin[2]) - self.baseViewer.viewerLogic.CoronalData.dimensions[2]\
                             * self.baseViewer.viewerLogic.CoronalData.spacing[2] / 2
            PickingCoords = (PickingCoords[0],PickingCoords[1],PickingCoordsZ)
            self.baseViewer.AddToLenPickingList(PickingCoords)


    def CursorStatus(self):
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.picker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            StartCursorPickingCoords = self.picker.GetPickPosition()
            # print(StartCursorPickingCoords)
            CusrerFocalPoint = self.baseViewer.Cursor.GetFocalPoint()
            if (abs(StartCursorPickingCoords[0]-CusrerFocalPoint[0]) <= 3*self.baseViewer.Cursor.GetRadius())\
                    and (abs(StartCursorPickingCoords[1]-CusrerFocalPoint[1]) <= self.baseViewer.Cursor.GetRadius()):
                self.actions["Cursor"] = 1
            else:
                self.actions["Cursor"] = 0

    def OnPickingCurserLeftButtonDown(self):
        pass

    def OnPickingCursorLeftButtonUp(self):
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.picker.Pick(mouseX, mouseY, 0.0, self.baseViewer.renderer):
            self.CurserPickingCoords = self.picker.GetPickPosition()
            self.baseViewer.viewerLogic.MoveCursor(self.CurserPickingCoords, self.viewMode)




