from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea, QAbstractItemView

from MRICenterline.app.database.openable_sessions import get_all_sessions

import logging
logging.getLogger(__name__)


class AnnotationLoadTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_item = None
        self.showing = 'ALL'

        self.resizeRowsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.clicked.connect(self.log_clicked_item)
        self.use_all_sessions()

    def use_all_sessions(self):
        self.showing = 'ALL'
        self.data, rows = get_all_sessions()
        self.setRowCount(rows)
        self.setColumnCount(len(self.data.keys()))
        self.set_data()

    def use_latest_sessions(self):
        self.showing = 'LAST'
        pass

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
        selected = self.selected_item
        return self.data['session_id'][selected]
