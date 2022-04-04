from MRICenterline.app.points.status import PickerStatus
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkInteractorStyleImage, vtkPropPicker


class CenterlineInteractorStyle(vtkInteractorStyleImage):
    point_picker = vtkPropPicker()

    def __init__(self,
                 model,
                 parent_interactor: QVTKRenderWindowInteractor = None):
        super().__init__()
        self.model = model
        self.parent = parent_interactor
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonEvent)

        self.AddObserver("MiddleButtonPressEvent", self.MiddleButtonEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.MiddleButtonEvent)

        self.AddObserver("RightButtonPressEvent", self.RightButtonEvent)
        self.AddObserver("RightButtonReleaseEvent", self.RightButtonEvent)

        self.AddObserver("MouseWheelForwardEvent", self.MouseWheelEvent)
        self.AddObserver("MouseWheelBackwardEvent", self.MouseWheelEvent)

        self.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        self.AddObserver("KeyPressEvent", self.KeyPressCallback)

    def LeftButtonEvent(self, obj, event):
        if self.model.picker_status == PickerStatus.NOT_PICKING:
            if event == 'LeftButtonPressEvent':
                vtkInteractorStyleImage.OnLeftButtonDown(self)
            elif event == 'LeftButtonReleaseEvent':
                vtkInteractorStyleImage.OnLeftButtonUp(self)
        else:
            if event == 'LeftButtonPressEvent':
                renderer = self.model.centerline_viewer.panel_renderer
                mouse_location = self.parent.GetEventPosition()
                if self.point_picker.Pick(*mouse_location, 0.0, renderer):
                    self.model.pick(self.point_picker.GetPickPosition())

    def MouseMoveCallback(self, obj, event):
        self.OnMouseMove()

        # renderer = self.model.sequence_viewer.panel_renderer
        # mouse_location = self.parent.GetEventPosition()
        # if self.point_picker.Pick(*mouse_location, 0.0, renderer):
        #     coords = self.point_picker.GetPickPosition()
        #     self.model.sequence_viewer.update_displayed_coords(coords)
        #     self.model.sequence_viewer.update_cursor_location(coords)

    def MiddleButtonEvent(self, obj, event):
        if event == "MiddleButtonPressEvent":
            vtkInteractorStyleImage.OnMiddleButtonDown(self)
        elif event == "MiddleButtonReleaseEvent":
            vtkInteractorStyleImage.OnMiddleButtonUp(self)

    def MouseWheelEvent(self, obj, event):
        shift = self.parent.GetShiftKey()
        if shift:
            if event == 'MouseWheelForwardEvent':
                self.model.adjust_height(1)
            elif event == "MouseWheelBackwardEvent":
                self.model.adjust_height(-1)
        else:
            if event == 'MouseWheelForwardEvent':
                self.model.adjust_angle(1)
            elif event == "MouseWheelBackwardEvent":
                self.model.adjust_angle(-1)

    def RightButtonEvent(self, obj, event):
        if event == "RightButtonPressEvent":
            vtkInteractorStyleImage.OnRightButtonDown(self)

        elif event == "RightButtonReleaseEvent":
            vtkInteractorStyleImage.OnRightButtonUp(self)

    def KeyPressCallback(self, obj, event):
        key_code = self.parent.GetKeyCode()
        key_symbol = self.parent.GetKeySym()
        # if key_code == 'h':
        #     self.model.sequence_viewer.toggle_help()
        # if key_code == "d":
        #     self.model.sequence_viewer.toggle_debug()
        # if key_code == 'c':
        #     self.model.sequence_viewer.toggle_cursor()
        #
        # if key_symbol == 'Up':
        #     self.model.sequence_viewer.adjust_slice_idx(1)
        # if key_symbol == "Down":
        #     self.model.sequence_viewer.adjust_slice_idx(-1)
