from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea, QAbstractItemView
from MRICenterline.app.points.status import PointStatus

import logging
logging.getLogger(__name__)


class PointsToTableView(QTableWidget):
    def __init__(self, model, parent=None):
        QTableWidget.__init__(self, parent)
        self.selected_item = None
        self.show = PointStatus.LENGTH
        self.model = model

        self.resizeRowsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.clicked.connect(self.log_clicked_item)
        self.show_length()

    def show_length(self):
        self.show = PointStatus.LENGTH
        self.data = self.model.length_point_array.generate_table_data()
        self.setRowCount(len(self.model.length_point_array))
        self.finalize_table()

    def show_mpr(self):
        self.show = PointStatus.MPR
        self.data = self.model.mpr_point_array.generate_table_data()
        # self.setRowCount(len(self.model.mpr_point_array))
        self.setRowCount(len(self.data['image coords']))
        self.finalize_table()

    def finalize_table(self):
        self.setColumnCount(3)
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_data(self):
        h_headers = []
        for n, key in enumerate(sorted(self.data.keys())):
            h_headers.append(key)
            for m, item in enumerate(self.data[key]):
                new_item = QTableWidgetItem(str(item))
                self.setItem(m, n, new_item)
        self.setHorizontalHeaderLabels(h_headers)

    def clear_table(self):
        self.setRowCount(0)

    def log_clicked_item(self, item):
        self.selected_item = item.row()
        logging.debug(f"Clicked {item.row()}")

    def get_data_for_selected(self):
        return self.data['physical coords'][self.selected_item], \
               self.data['itk indices'][self.selected_item], \
               self.data['image coords'][self.selected_item], \
               self.selected_item
