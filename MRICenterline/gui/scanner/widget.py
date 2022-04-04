from pathlib import Path
from glob import glob
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel, \
                            QGridLayout, QTextEdit, QGroupBox, QCheckBox

from MRICenterline import CFG
from MRICenterline.app import scanner

import logging
logging.getLogger(__name__)


class ScannerWidget(QWidget):
    folder_path = CFG.get_folder('raw_data')
    text_box = QTextEdit()
    preprocess_options = {
        "organize_data":
            QCheckBox("Reorganize the data (generic case names, flat structure)"),
        "metadata_sequence_scan":
            QCheckBox("Scan the files for metadata and sequences and commits to database")
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.directories = [Path(i) for i in glob(f"{self.folder_path}/**/", recursive=True)]
        self.directories.remove(Path(self.folder_path))

        main_layout = QGridLayout(self)
        self.status_text = f"<font color='red'>Found {len(self.directories)} directories in "\
                           f"{self.folder_path}</font>"

        self.text_box.setHtml(self.status_text)

        # main layout
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 2)
        main_layout.setRowStretch(2, 1)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 1)

        # inner layout
        inner_layout = QVBoxLayout()

        main_layout.addLayout(inner_layout, 1, 1, 1, 1)

        # preprocessing
        self.preprocess_options['organize_data'].setChecked(False)
        self.preprocess_options['organize_data'].setEnabled(False)

        self.preprocess_options['metadata_sequence_scan'].setChecked(True)

        preprocess_options_group_box = QGroupBox("Bulk Scanner Options")
        preprocess_options_layout = QVBoxLayout()
        preprocess_options_group_box.setLayout(preprocess_options_layout)

        preprocess_options_layout.addWidget(self.preprocess_options['organize_data'])
        preprocess_options_layout.addWidget(self.preprocess_options['metadata_sequence_scan'])

        preprocess_button = QPushButton("Start")
        preprocess_options_layout.addWidget(preprocess_button)

        preprocess_button.clicked.connect(self.connect_options)

        inner_layout.addWidget(preprocess_options_group_box)

        # export
        export_group_box = QGroupBox("Export from database to CSV")
        export_layout = QVBoxLayout()
        export_group_box.setLayout(export_layout)

        time_export_button = QPushButton("Export time data")
        time_export_button.clicked.connect(lambda: self.connect_export('time'))
        export_layout.addWidget(time_export_button)

        time_export_button = QPushButton("Export metadata")
        time_export_button.clicked.connect(lambda: self.connect_export('metadata'))
        export_layout.addWidget(time_export_button)

        time_export_button = QPushButton("Export sequence report")
        time_export_button.clicked.connect(lambda: self.connect_export('sequence'))
        export_layout.addWidget(time_export_button)

        inner_layout.addWidget(export_group_box)

        inner_layout.addWidget(QLabel("Status: "))
        inner_layout.addWidget(self.text_box)

    def connect_export(self, opt):
        path = QFileDialog(self).getSaveFileName(filter="*.csv")[0]

        if path:
            if opt == 'time':
                scanner.run_time_report("")
            elif opt == 'metadata':
                pass
            elif opt == 'sequence':
                pass

    def connect_options(self):
        opts_for_logger = [opt.isChecked() for opt in self.preprocess_options.values()]
        logging.info(f"Running scanner with {opts_for_logger}")

        if self.preprocess_options['organize_data'].isChecked():
            scanner.run_organize_data("", "", parent_widget=self)
        if self.preprocess_options['metadata_sequence_scan'].isChecked():
            scanner.run_metadata_sequence_scan(self.directories, parent_widget=self)

    def add_to_textbox(self, text, color=None):
        if color:
            self.status_text += f"<p><font color={color}> {text} </font></p>"
        else:
            self.status_text += f"<p> {text} </p>"
        self.text_box.setHtml(self.status_text)
