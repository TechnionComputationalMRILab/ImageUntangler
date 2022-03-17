from PyQt5.QtWidgets import QDialog, QVBoxLayout, \
    QDialogButtonBox, QCheckBox, QHBoxLayout

from MRICenterline.gui.loader.annotation.table import AnnotationLoadTable

import logging
logging.getLogger(__name__)


class AnnotationLoadDialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = AnnotationLoadTable(parent=self)
        buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        bottom_layout = QHBoxLayout()
        show_most_recent_checkbox = QCheckBox("Show only most recent")
        show_most_recent_checkbox.setEnabled(True)
        show_most_recent_checkbox.clicked.connect(self.show_most_recent)
        bottom_layout.addWidget(show_most_recent_checkbox)
        bottom_layout.addWidget(buttons)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.table)
        main_layout.addLayout(bottom_layout)

    def show_most_recent(self, s):
        if s:
            print('showing recents')
        else:
            print('showing all')

    def accept(self):
        super().accept()

    def get_file(self):
        return "aaa"
