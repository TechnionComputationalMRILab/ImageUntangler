from MRICenterline.app.points.status import PointStatus

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea


class PointsToTableView(QTableWidget):
    def __init__(self, model, parent=None):
        QTableWidget.__init__(self, parent)
        self.show = PointStatus.LENGTH
        self.model = model

        self.show_length()

    def show_length(self):
        self.show = PointStatus.LENGTH
        self.data = self.model.length_point_array.generate_table_data()
        self.setRowCount(len(self.model.length_point_array))
        self.finalize_table()

    def show_mpr(self):
        self.show = PointStatus.MPR
        self.data = self.model.mpr_point_array.generate_table_data()
        self.setRowCount(len(self.model.mpr_point_array))
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
