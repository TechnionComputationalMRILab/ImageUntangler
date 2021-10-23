import os

from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QTextEdit

from MRICenterline.PatientInfo.PatientTable import PatientTable

import logging
logging.getLogger(__name__)


class PatientInfoPanel(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # self._table = PatientTable(parent=self)
        # self._buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        # self._buttons.accepted.connect(self.accept)
        # self._buttons.rejected.connect(self.reject)

        self._comment_box = QTextEdit()
        self._comment_box.setHtml("Comments here")

        self._v_layout = QVBoxLayout(self)
        # self._v_layout.addWidget(self._table)
        self._v_layout.addWidget(self._comment_box)
