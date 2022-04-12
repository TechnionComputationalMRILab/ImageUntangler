from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QCheckBox, QVBoxLayout

from MRICenterline.gui.points.table import PointsToTableView

from MRICenterline.app.gui_data_handling.sequence_model import SequenceModel
from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class PointDialogBox(QDialog):
    def __init__(self, model: SequenceModel, parent=None):
        super().__init__(parent)
        self.selected_point_index = None
        self.selected_point_type = None

        self.table = PointsToTableView(model, self)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.toggle = QCheckBox("Show MPR points")
        self.toggle.clicked.connect(self.toggle_table)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.buttons)
        layout.addWidget(self.toggle)

    def toggle_table(self, s):
        if s:
            self.toggle.setText("Show Length points")
            self.table.clear_table()
            self.table.show_mpr()
        else:
            self.toggle.setText("Show MPR points")
            self.table.clear_table()
            self.table.show_length()

    def accept(self) -> None:
        if type(self.table.selected_item) is int:

            _, _, _, self.selected_point_index = self.table.get_data_for_selected()
            self.selected_point_type = self.table.show
            super().accept()
        else:
            logging.debug("None selected")
            super().reject()
