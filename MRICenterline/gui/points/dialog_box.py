from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import Qt

from MRICenterline.gui.points.table import PointsToTableView

from MRICenterline.app.gui_data_handling.sequence_model import SequenceModel
from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class PointDialogBox(QDialog):
    def __init__(self, model: SequenceModel, parent=None):
        super().__init__(parent)
        self.model = model
        self.length_data = model.length_point_array.generate_table_data()
        self.mpr_data = model.mpr_point_array.generate_table_data()

        layout = QVBoxLayout(self)

        length_table_widget = PointsToTableView(self.length_data, len(model.length_point_array), 3)
        layout.addWidget(length_table_widget)
