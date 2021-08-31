from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QVBoxLayout, QLabel, \
                            QGridLayout, QTextEdit

from . import Scanner

import logging
logging.getLogger(__name__)


class ProgressWidget(QWidget):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)

        self.folder_path = folder_path
        self.directories = Scanner.get_directories(self.folder_path)
        self._grid_layout = QGridLayout(self)
        self.status_text = f"<font color='red'>Found {len(self.directories)} directories in "\
                           f"{self.folder_path}</font>"

        self.set_up_main_layout()
        self.set_up_inner_layout()

    def set_up_main_layout(self):
        self._grid_layout.setRowStretch(0, 1)
        self._grid_layout.setRowStretch(1, 2)
        self._grid_layout.setRowStretch(2, 1)

        self._grid_layout.setColumnStretch(0, 1)
        self._grid_layout.setColumnStretch(1, 1)
        self._grid_layout.setColumnStretch(2, 1)

    def set_up_inner_layout(self):
        self._v_layout = QVBoxLayout()

        _warning = QLabel()
        _warning.setText("Bulk folder scanner: Creates sequence dictionaries for several folders at a time.")
        _warning.setWordWrap(True)

        # self.file_system_model = QFileSystemModel()
        # self.file_system_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        # self.file_system_model.setRootPath(self.folder_path)
        #
        # self.tree_view = QTreeView()
        # self.tree_view.setModel(self.file_system_model)
        # self.tree_view.setRootIndex(self.file_system_model.index(self.folder_path, column=0))
        # self.tree_view.setColumnWidth(0, 500)
        # self.tree_view.hideColumn(1)
        # self.tree_view.hideColumn(2)

        self.text_box = QTextEdit()
        self.text_box.setHtml(self.status_text)

        self._add_to_textbox("<b>Does not currently support sequences with different patients in the same "
                             "directory.</b>", color='red')

        _start_button = QPushButton("Start")
        _start_button.setMinimumSize(600, 200)
        _start_button.clicked.connect(self.scan)

        self._v_layout.addWidget(_warning)
        self._v_layout.addWidget(self.text_box)
        self._v_layout.addWidget(_start_button)

        if len(self.directories) > 1:
            self.prog_bar = QProgressBar(self)
            self.prog_bar.setMaximum(len(self.directories) - 1)
            self._v_layout.addWidget(self.prog_bar)

        self._grid_layout.addLayout(self._v_layout, 1, 1, 1, 1)

    def scan(self):
        logging.info("Starting folder scan")
        self._add_to_textbox("Starting scan!")

        for i, val in enumerate(self.directories):
            Scanner.generate_seq_dict(val)
            self._add_to_textbox(f"<b>[Folder {i+1}/{len(self.directories)}]</b>: {val}")

            if len(self.directories) > 1:
                self.prog_bar.setValue(i)

        self._add_to_textbox("Done! You can close this tab now", color='blue')

    def _add_to_textbox(self, text, color=None):
        if color:
            self.status_text += f"<p><font color={color}> {text} </font></p>"
        else:
            self.status_text += f"<p> {text} </p>"
        self.text_box.setHtml(self.status_text)
