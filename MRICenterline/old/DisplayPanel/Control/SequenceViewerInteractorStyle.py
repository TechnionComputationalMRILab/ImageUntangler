from vtkmodules.all import vtkInteractorStyleImage, vtkPropPicker
# from icecream import ic

import vtkmodules.all as vtk

import logging
logging.getLogger(__name__)


class SequenceViewerInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, parent, model):
        super().__init__()
        self.model = model
        self.parent = parent
        self.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        self.AddObserver("MiddleButtonPressEvent", self.ButtonCallback)
        self.AddObserver("MiddleButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonPressEvent", self.ButtonCallback)
        self.AddObserver("LeftButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("RightButtonPressEvent", self.ButtonCallback)
        self.AddObserver("RightButtonReleaseEvent", self.ButtonCallback)
        self.AddObserver("KeyPressEvent", self.KeyPressCallback)
        self.AddObserver("MouseWheelForwardEvent", self.MouseWheelForwardCallback)
        self.AddObserver("MouseWheelBackwardEvent", self.MouseWheelBackwardCallback)

        ## Create callbacks for slicing the image
        self.actions = dict()
        self.actions["Slicing"] = 0
        self.actions["Windowing"] = 0
        self.actions["Zooming"] = 0
        self.actions["PickingMPR"] = 0
        self.actions["PickingLength"] = 0
        self.actions["ModifyingMPRAnnotation"] = 0
        self.actions["Cursor"] = 0
        self.actions["Panning"] = 0
        self.actions['EditingMPR'] = 0

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
                SequenceViewerInteractorStyle.OnPickingCurserLeftButtonDown(self)
            elif self.actions["PickingMPR"] == 1 or self.actions["PickingLength"] == 1:
                SequenceViewerInteractorStyle.OnPickingLeftButtonDown(self)

        elif event == "LeftButtonReleaseEvent":
            (mouseX, mouseY) = self.parent.GetEventPosition()
            if self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 0:
                self.actions["Windowing"] = 0
                vtkInteractorStyleImage.OnLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 0 and self.actions["PickingLength"] == 0 and self.actions["Cursor"] == 1:
                self.actions["Cursor"] = 0
                SequenceViewerInteractorStyle.OnPickingCursorLeftButtonUp(self)
            elif self.actions["PickingMPR"] == 1:
                SequenceViewerInteractorStyle.pickImagePoint(self, "MPR", mouseX, mouseY)
            elif self.actions["PickingLength"] == 1:
                SequenceViewerInteractorStyle.pickImagePoint(self, "Length", mouseX, mouseY)

    def MouseMoveCallback(self, obj, event):
        (lastX, lastY) = self.parent.GetLastEventPosition()
        (mouseX, mouseY) = self.parent.GetEventPosition()

        try:
            displayed_coords = SequenceViewerInteractorStyle.pickImagePoint(self, "None", mouseX, mouseY, query=True)
            self.model.updateDisplayedCoords(displayed_coords)
        except:
            pass

        if self.actions["Slicing"] == 1:
            deltaY = mouseY - lastY
            self.model.changeSliceIndex(deltaY)

        elif self.actions["Windowing"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            self.model.updateWindowLevel()

        elif self.actions["Zooming"] == 1:
            vtkInteractorStyleImage.OnMouseMove(self)
            self.model.updateZoomFactor()
        else:
            self.OnMouseMove() # call to superclass

    def KeyPressCallback(self, obj, event):
        logging.info(f'Keycode entered: {self.parent.GetKeyCode()}')

        if self.parent.GetKeyCode() == 'C' or self.parent.GetKeyCode() == 'c':  # cursor
            if self.ShowCursor:
                self.ShowCursor = False
                self.model.clearCursor()
            else:
                self.ShowCursor = True
                self.model.addCursor()

        elif self.parent.GetKeyCode() == 'p' or self.parent.GetKeyCode() == 'P':  # pick
            (mouseX, mouseY) = self.parent.GetEventPosition()

            points = self.pickImagePoint("Editing", mouseX, mouseY, query=True)
            # ic(points)
            # x, y = points[0:2]

            self.model.modifyAnnotation(mouseX, mouseY)
            # turn on point picking

        elif self.parent.GetKeyCode() == 'Q' or self.parent.GetKeyCode() == 'q':  # query
            pass
            # ic(self.parent.GetEventPosition())

        elif self.parent.GetKeyCode() == 'd' or self.parent.GetKeyCode() == 'D':  # delete
            x, y = self.parent.GetEventPosition()
            _prop = self.model.modifyAnnotation(x, y)

            self.model.deleteAnnotation(x, y, _prop)

        elif self.parent.GetKeySym() == 'Up':
            self.model.changeSliceIndex(1)
        elif self.parent.GetKeySym() == 'Down':
            self.model.changeSliceIndex(-1)

    def cursorInBullsEye(self) -> int:
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.model.view.panel_renderer):
            StartCursorPickedCoordinates = self.pointPicker.GetPickPosition()
            cursorFocalPoint = self.model.view.Cursor.GetFocalPoint()
            if (abs(StartCursorPickedCoordinates[0]-cursorFocalPoint[0]) <= 3*self.model.view.Cursor.GetRadius())\
                    and (abs(StartCursorPickedCoordinates[1]-cursorFocalPoint[1]) <= self.model.view.Cursor.GetRadius()):
                return 1
            else:
                return 0

    def pickImagePoint(self, pointType: str, mouseX, mouseY, query=False):
        # print(mouseX, mouseY)
        _pick = self.pointPicker.Pick(mouseX, mouseY, 0.0, self.model.view.panel_renderer)
        if _pick:
            pickPosition = self.pointPicker.GetPickPosition()

            # zCoordinate = self.model.view.z_coords[self.model.view.sliceIdx]
            zCoordinate = 1 + self.model.view.imageData.size[2] - self.model.view.sliceIdx
            pickedCoordinates = (pickPosition[0], pickPosition[1], zCoordinate)

            if query:
                return pickedCoordinates
            else:
                self.model.addPoint(pointType, pickedCoordinates)

    def OnPickingCursorLeftButtonUp(self):
        (mouseX, mouseY) = self.parent.GetEventPosition()
        if self.pointPicker.Pick(mouseX, mouseY, 0.0, self.model.view.panel_renderer):
            cursorPickedCoordinates = self.pointPicker.GetPickPosition()
            self.model.moveBullsEye(cursorPickedCoordinates)

    def OnPickingCurserLeftButtonDown(self):
        pass

    def MouseWheelForwardCallback(self, obj,event):
        self.model.changeSliceIndex(1)

    def MouseWheelBackwardCallback(self, obj,event):
        self.model.changeSliceIndex(-1)

    def OnPickingLeftButtonDown(self):
        pass


