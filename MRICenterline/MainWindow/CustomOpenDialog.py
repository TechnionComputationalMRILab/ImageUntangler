import os
import csv
from copy import copy
from collections import defaultdict
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QAbstractScrollArea, QAbstractItemView, QDialogButtonBox
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class CustomOpenTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_item = None

        self._directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'report.csv')
        if not os.path.exists(self._directory):
            MSG.msg_box_warning("Saved Points Directory does not exist yet!")
            logging.critical("Tried to load without directory")
            raise FileNotFoundError
        else:
            logging.info("Opening report.csv")

            _columns = defaultdict(list)
            _num_of_rows = 0

            with open(self._directory, 'r') as f:
                _reader = csv.DictReader(f)
                for row in _reader:  # read a row as {column1: value1, column2: value2,...}
                    _num_of_rows += 1
                    for (k, v) in row.items():  # go over each column name and value
                        _columns[k].append(v)  # append the value into the appropriate list
                        # based on column name k

            [_columns.pop(i) for i in ['PatientName', 'PatientID', 'ManufacturerModelName', 'ProtocolName', 'StudyTime']]

            _columns["Path"] = [file.replace('\\', '/') for file in _columns["Path"]]
            self.path_list = copy(_columns['Path'])
            _columns["Path"] = [i.split("/")[-2] for i in _columns["Path"]]

            self.data = {k: _columns[k] for k in ['Path', 'StudyDate', 'Manufacturer', 'Sequences']}
            # self.data = _columns

        self.setRowCount(_num_of_rows)
        self.setColumnCount(4)

        self.set_data()
        # self.resizeColumnsToContents()
        self.setColumnWidth(3, 1000)
        self.resizeRowsToContents()

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.clicked.connect(self._log_clicked_item)

    def set_data(self):
        _horizontal_headers = []
        for n, key in enumerate(self.data.keys()):
            _horizontal_headers.append(key)
            for m, item in enumerate(self.data[key]):
                _table_item = QTableWidgetItem(item)
                self.setItem(m, n, _table_item)
        self.setHorizontalHeaderLabels(_horizontal_headers)

    def _log_clicked_item(self, item):
        self.selected_item = item.row()
        logging.debug(f"Clicked {item.row()}")


class CustomOpenDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._table = CustomOpenTable(parent=self)
        self._buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self._v_layout = QVBoxLayout(self)
        self._v_layout.addWidget(self._table)
        self._v_layout.addWidget(self._buttons)

        self.full_path = None

    def accept(self) -> None:
        if type(self._table.selected_item) is int:
            logging.debug(f"Opening {self._table.selected_item}")

            self.full_path = self._table.path_list[self._table.selected_item]

            super().accept()
        else:
            logging.debug("None selected")
            super().reject()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dlg = CustomOpenDialog()
    dlg.exec()

    print(dlg.full_path)
    sys.exit(app.exec())
