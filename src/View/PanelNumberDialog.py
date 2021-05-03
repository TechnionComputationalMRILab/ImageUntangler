from PyQt5.QtWidgets import *


class PanelNumberDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.panel_number = 2, 0

        self.setWindowTitle("Set number of panels")

        _qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(_qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.groupbox = QGroupBox("Set number of panels")
        self.setLayout(self.layout)

        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.buttonBox)

        self.groupbox_layout = QGridLayout()
        self.groupbox.setLayout(self.groupbox_layout)
        self.groupbox_layout.addWidget(QLabel("Horizontal"), 1, 1)
        self.groupbox_layout.addWidget(QLabel("Vertical"), 2, 1)

        self.horizontal_spinbox = QDoubleSpinBox()
        self.vertical_spinbox = QDoubleSpinBox()

        self.horizontal_spinbox.setValue(2)
        self.horizontal_spinbox.setDecimals(0)
        self.vertical_spinbox.setDecimals(0)

        self.groupbox_layout.addWidget(self.horizontal_spinbox, 1, 2)
        self.groupbox_layout.addWidget(self.vertical_spinbox, 2, 2)

        self.show()

    def accept(self) -> None:
        _total_number_of_panels = self.horizontal_spinbox.value() + self.vertical_spinbox.value()
        if _total_number_of_panels == 0:
            QMessageBox.information(self, "Error", 'Need more than 1 panel!')
        else:
            self.panel_number = int(self.horizontal_spinbox.value()), int(self.vertical_spinbox.value())
            super().accept()
