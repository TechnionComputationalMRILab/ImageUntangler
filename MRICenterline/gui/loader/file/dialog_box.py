from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, \
    QDialogButtonBox, QCheckBox

from MRICenterline.gui.loader.file.table import SequenceFileOpenTable
from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class FileOpenDialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_case, self.selected_sequence = None, None
        self.table = SequenceFileOpenTable(self)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.toggle_style = QCheckBox("Show by case metadata")
        self.toggle_style.clicked.connect(self.toggle_table)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.buttons)
        layout.addWidget(self.toggle_style)

    def get_file(self):
        return Path(CFG.get_folder('raw') + "/" + self.selected_case), self.selected_sequence

    def toggle_table(self, s):
        if s:
            self.toggle_style.setText("Show by case sequences")
            self.table.clear_table()
            self.table.use_cases()
        else:
            self.toggle_style.setText("Show by case metadata")
            self.table.clear_table()
            self.table.use_sequences()

    def accept(self) -> None:
        if type(self.table.selected_item) is int:

            self.selected_case, self.selected_sequence = self.table.get_data_for_selected()
            super().accept()
        else:
            logging.debug("None selected")
            super().reject()
