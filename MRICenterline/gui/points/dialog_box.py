from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QCheckBox, QVBoxLayout
from PyQt5.Qt import Qt

from MRICenterline.gui.points.table import PointsToTableView

from MRICenterline.app.gui_data_handling.sequence_model import SequenceModel
from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class PointDialogBox(QDialog):
    def __init__(self, model: SequenceModel, parent=None):
        super().__init__(parent)

        self.table = PointsToTableView(model, self)

        self.toggle = QCheckBox("Show MPR points")
        self.toggle.clicked.connect(self.toggle_table)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
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
