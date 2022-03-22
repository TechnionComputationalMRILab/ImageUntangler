from MRICenterline.app.points.status import PickerStatus
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkInteractorStyleImage, vtkPropPicker


class CenterlineInteractorStyle(vtkInteractorStyleImage):
    point_picker = vtkPropPicker()

    def __init__(self,
                 model,
                 parent_interactor: QVTKRenderWindowInteractor = None):
        super().__init__()
