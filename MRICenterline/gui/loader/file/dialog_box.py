from PyQt5.QtWidgets import QDialog, QVBoxLayout, \
    QDialogButtonBox

from MRICenterline.gui.loader.file.table import FileOpenTable

import logging
logging.getLogger(__name__)


class FileOpenDialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._table = FileOpenTable(parent=self)
        self._buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self._v_layout = QVBoxLayout(self)
        self._v_layout.addWidget(self._table)
        self._v_layout.addWidget(self._buttons)

        self.full_path = None

    def accept(self):
        super().accept()

    def get_file(self):
        return "aa"
