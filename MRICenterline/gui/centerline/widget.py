from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel

from MRICenterline.app.centerline.centerline_model import CenterlineModel
from MRICenterline.gui.vtk.centerline_interactor_style import CenterlineInteractorStyle
from MRICenterline.app.gui_data_handling.centerline_viewer import CenterlineViewer


class CenterlineWidget(QWidget):
    text = "test"

    def __init__(self, model: CenterlineModel, parent=None):
        super().__init__(parent)
        self.model = model
        layout = QVBoxLayout(self)

        self._frame = QGroupBox()
        self.interactor = QVTKRenderWindowInteractor(self._frame)
        self.interactor_style = CenterlineInteractorStyle(model=self.model, parent_interactor=self.interactor)

        self.centerline_viewer = CenterlineViewer(self.model, self.interactor, self.interactor_style)
        self.model.connect_viewer(self.centerline_viewer)

        self.label = QLabel(self.text)
        layout.addWidget(self.label)
        layout.addWidget(self.interactor)

