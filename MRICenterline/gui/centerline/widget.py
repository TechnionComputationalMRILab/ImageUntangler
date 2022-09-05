from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel

from MRICenterline.app.gui_data_handling.centerline_model import CenterlineModel
from MRICenterline.gui.vtk.centerline_interactor_style import CenterlineInteractorStyle
from MRICenterline.app.gui_data_handling.centerline_viewer import CenterlineViewer


class CenterlineWidget(QWidget):
    text = "No points selected"

    def __init__(self, model: CenterlineModel, parent=None):
        super().__init__(parent)
        self.parent = parent
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

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        self.interactor.Finalize()

    def change_widget_text(self, text):
        self.label.setText(text)
