import os
import csv
from collections import defaultdict
from itertools import groupby

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QAbstractScrollArea, QAbstractItemView, QDialogButtonBox, QCheckBox, QHBoxLayout
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class LoadDirTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSortingEnabled(True)
        self.selected_item = None
        self._raw_data = []

        self._directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'directory.csv')
        if not os.path.exists(self._directory):
            MSG.msg_box_warning("Saved Points Directory does not exist yet!")
            logging.critical("Tried to load without directory")
            raise FileNotFoundError
        else:
            logging.info("Opening directory.csv")

            _columns = defaultdict(list)
            _num_of_rows = 0

            with open(self._directory, 'r') as f:
                _reader = csv.DictReader(f)
                for row in _reader:                 # read a row as {column1: value1, column2: value2,...}

                    self._raw_data.append(row.items())
                    _num_of_rows += 1
                    for (k, v) in row.items():      # go over each column name and value
                        _columns[k].append(v)       # append the value into the appropriate list
                                                    # based on column name k
            self.file_list = _columns.pop('filename')
            self.path_list = _columns.pop('path')
            self.data = {k: _columns[k] for k in ['case number', 'sequence name', "date", 'has CL',
                                                  '# MPR points', '# len points', 'Time measurement', 'length']}

        # self.hidden_rows = self._get_latest_cases()

        self.setRowCount(_num_of_rows)
        self.setColumnCount(8)

        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.clicked.connect(self._log_clicked_item)

    def _get_latest_cases(self):
        # group cases together
        _raw_data_as_list_of_dicts = []
        for k, v in enumerate(self._raw_data):
            _temp_dict = dict(v)
            _temp_dict["index"] = k
            _raw_data_as_list_of_dicts.append(_temp_dict)

        _raw_data_as_list_of_dicts.sort(key=lambda x: x['case number'])

        _grouped_cases = []
        for k, v in groupby(_raw_data_as_list_of_dicts, key=lambda x: x['case number']):
            _grouped_cases.append({k: list(v)})

        for i in _grouped_cases:
            for k, v in i:
            # _temp.sort(key=lambda x: x['date'])
                print(v)

        # get latest date

        # get indices

        return [0, 1]

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

    def show_only_recent(self):
        for i in self.hidden_rows:
            self.showRow(i)

    def show_all(self):
        for i in self.hidden_rows:
            self.hideRow(i)


class LoadDirDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._table = LoadDirTable(parent=self)
        self._buttons = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self._bottom_layout = QHBoxLayout()
        self._show_most_recent_checkbox = QCheckBox("Show only most recent")
        self._show_most_recent_checkbox.setEnabled(False)
        self._show_most_recent_checkbox.clicked.connect(self.show_most_recent)
        self._bottom_layout.addWidget(self._show_most_recent_checkbox)
        self._bottom_layout.addWidget(self._buttons)

        self._v_layout = QVBoxLayout(self)
        self._v_layout.addWidget(self._table)
        self._v_layout.addLayout(self._bottom_layout)

        self.path = {'path': None, 'file': None, 'full_path': None}

    def show_most_recent(self):
        if self._show_most_recent_checkbox.isChecked():
            self._table.show_only_recent()
        else:
            self._table.show_all()

    def accept(self) -> None:
        if type(self._table.selected_item) is int:
            logging.debug(f"Opening {self._table.selected_item}")

            self.path = {'path': self._table.path_list[self._table.selected_item],
                         'file': self._table.file_list[self._table.selected_item],
                         'full_path': os.path.join(self._table.path_list[self._table.selected_item], "data", self._table.file_list[self._table.selected_item])
                         }

            super(LoadDirDialog, self).accept()
        else:
            logging.debug("None selected")
            super(LoadDirDialog, self).reject()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = LoadDirDialog()
    win.show()
    sys.exit(app.exec())
