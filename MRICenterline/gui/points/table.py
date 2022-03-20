from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class PointsToTableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.set_data()

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def set_data(self):
        h_headers = []
        for n, key in enumerate(sorted(self.data.keys())):
            h_headers.append(key)
            for m, item in enumerate(self.data[key]):
                new_item = QTableWidgetItem(str(item))
                self.setItem(m, n, new_item)
        self.setHorizontalHeaderLabels(h_headers)
