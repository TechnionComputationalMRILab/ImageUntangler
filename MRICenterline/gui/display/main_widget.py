from PyQt5.QtWidgets import QWidget, QVBoxLayout


class MainDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

    def configure_widgets(self, sequence_widgets, vtk_widget):
        self.main_layout.addWidget(sequence_widgets.sequence_combo_box)
        self.main_layout.addWidget(vtk_widget)
        self.main_layout.addLayout(sequence_widgets.build_group_box())
