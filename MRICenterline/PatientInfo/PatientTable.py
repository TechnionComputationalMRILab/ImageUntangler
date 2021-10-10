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


class PatientTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            self.data = {k: _columns[k] for k in ['case number', "date", 'number of MPR points', 'sequence name']}

        # self.hidden_rows = self._get_latest_cases()

        self.setRowCount(_num_of_rows)
        self.setColumnCount(4)

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

