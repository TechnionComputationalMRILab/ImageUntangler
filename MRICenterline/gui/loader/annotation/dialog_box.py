from PyQt5.QtWidgets import QDialog, QVBoxLayout, \
    QDialogButtonBox, QCheckBox, QHBoxLayout

from MRICenterline.gui.loader.annotation.table import AnnotationLoadTable

import logging
logging.getLogger(__name__)


class AnnotationLoadDialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_session = None

        self.table = AnnotationLoadTable(parent=self)
        buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.toggle_style = QCheckBox("Show only most recent")
        self.toggle_style.clicked.connect(self.toggle_table)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(buttons)
        layout.addWidget(self.toggle_style)

    def toggle_table(self, s):
        if s:
            self.toggle_style.setText("Show all annotations")
        else:
            self.toggle_style.setText("Show only most recent")

    def accept(self):
        if type(self.table.selected_item) is int:

            self.selected_session = self.table.get_data_for_selected()
            super().accept()
        else:
            logging.debug("None selected")
            super().reject()

    def get_session(self):
        return self.selected_session
