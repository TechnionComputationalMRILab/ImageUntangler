from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox, \
    QFileDialog, QPushButton
from PyQt5.Qt import Qt

from MRICenterline import CFG

import logging

from MRICenterline.app.export import ExportType

logging.getLogger(__name__)


class ExportDialogBox(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.parent = parent
        self.destination = None

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # display export

        self.display_export_box = QGroupBox("Export Display image as")
        self.display_export_box.setCheckable(True)
        layout.addWidget(self.display_export_box)

        display_export_layout = QVBoxLayout()
        self.display_export_box.setLayout(display_export_layout)

        self.display_format_buttons = []
        for fmt in ExportType:
            radiobutton = QRadioButton(fmt.value)
            display_export_layout.addWidget(radiobutton)
            self.display_format_buttons.append((fmt, radiobutton))

        self.display_length = QCheckBox("Include Length Measurements")
        display_export_layout.addWidget(self.display_length)

        self.display_annotation = QCheckBox("Include Annotations")
        display_export_layout.addWidget(self.display_annotation)

        # centerline export

        self.centerline_export_box = QGroupBox("Export centerline image as")
        self.centerline_export_box.setCheckable(True)
        layout.addWidget(self.centerline_export_box)

        centerline_export_layout = QVBoxLayout()
        self.centerline_export_box.setLayout(centerline_export_layout)

        self.centerline_format_buttons = []
        for fmt in ExportType:
            radiobutton = QRadioButton(fmt.value)
            centerline_export_layout.addWidget(radiobutton)
            self.centerline_format_buttons.append((fmt, radiobutton))

        self.centerline_length = QCheckBox("Include Length Measurements")
        centerline_export_layout.addWidget(self.centerline_length)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.select_destination)
        buttons.accepted.connect(self.compile_export_options)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def select_destination(self):
        self.destination = str(QFileDialog.getExistingDirectory(self.parent, "Select destination"))
        logging.info(f"Exporting to {self.destination}")

    def compile_export_options(self):
        display_export_options = dict()
        centerline_export_options = dict()

        if self.display_export_box.isChecked():
            for fmt, button in self.display_format_buttons:
                if button.isChecked():
                    display_export_options['format'] = fmt

            display_export_options['length'] = self.display_length.isChecked()
            display_export_options['annotation'] = self.display_annotation.isChecked()

        if self.centerline_export_box.isChecked():
            for fmt, button in self.centerline_format_buttons:
                if button.isChecked():
                    centerline_export_options['format'] = fmt

            centerline_export_options['length'] = self.centerline_length.isChecked()

        self.model.export(self.destination, display_export_options, centerline_export_options)
