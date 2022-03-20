from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QShortcut, QLabel
from PyQt5.QtGui import QKeySequence


class CenterlineWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel('Centerline Panel test'))
