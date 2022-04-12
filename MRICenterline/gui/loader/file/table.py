from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea, QAbstractItemView
from MRICenterline.app.database.openable_files import get_openable_sequences, get_openable_cases

import logging
logging.getLogger(__name__)


class SequenceFileOpenTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_item = None
        self.showing = 'SEQ'

        self.resizeRowsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.clicked.connect(self.log_clicked_item)
        self.use_sequences()

    def use_sequences(self):
        self.showing = 'SEQ'
        self.data, rows = get_openable_sequences()
        self.setRowCount(rows)
        self.setColumnCount(3)
        self.set_data()
        self.setColumnWidth(1, 500)

    def use_cases(self):
        self.showing = 'CASE'
        self.data, columns, rows = get_openable_cases()
        self.setRowCount(rows)
        self.setColumnCount(columns)
        self.set_data()

    def set_data(self):
        h_headers = []
        for n, key in enumerate(sorted(self.data.keys())):
            h_headers.append(key)
            for m, item in enumerate(self.data[key]):
                new_item = QTableWidgetItem(str(item))
                self.setItem(m, n, new_item)
        self.setHorizontalHeaderLabels(h_headers)

    def log_clicked_item(self, item):
        self.selected_item = item.row()
        logging.debug(f"Clicked {item.row()}")

    def clear_table(self):
        self.setRowCount(0)

    def get_data_for_selected(self):
        if self.showing == "SEQ":
            return self.data['case_name'][self.selected_item], self.data['sequences'][self.selected_item]
        elif self.showing == "CASE":
            return self.data['case_name'][self.selected_item], None

