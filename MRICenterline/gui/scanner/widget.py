from pathlib import Path
from glob import glob

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel, \
                            QGridLayout, QTextEdit, QGroupBox, QCheckBox, QProgressBar

from MRICenterline import CFG
from MRICenterline.app import scanner
from MRICenterline.gui.scanner.worker import ScanWorker

import logging
logging.getLogger(__name__)


class ScannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.folder_path = CFG.get_folder('raw_data')
        self.text_box = QTextEdit()
        self.preprocess_options = {
            "organize_data":
                QCheckBox("Reorganize the data (generic case names, flat structure)"),
            "metadata_sequence_scan":
                QCheckBox("Scan the files for metadata and sequences and commits to database")
        }

        self.thread = QThread()
        self.worker = None

        # self.directories = [Path(i) for i in glob(f"{self.folder_path}/**/", recursive=True)]
        # self.files = Path(self.folder_path).rglob("*")
        # try:
        #     self.directories.remove(Path(self.folder_path))
        # except ValueError:
        #     # user selected a directory in a way that the root folder is not in the list
        #     pass

        # region view
        main_layout = QGridLayout(self)
        self.status_text = f"<font color='red'>Reading from {self.folder_path}</font>"

        self.text_box.setHtml(self.status_text)
        self.add_to_textbox("GUI scanner is partially disabled in this version")

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

        self.preprocess_button = QPushButton("Start")
        preprocess_options_layout.addWidget(self.preprocess_button)

        self.preprocess_button.clicked.connect(self.connect_options)

        inner_layout.addWidget(preprocess_options_group_box)

        # export
        export_group_box = QGroupBox("Export from database to CSV")
        export_layout = QVBoxLayout()
        export_group_box.setLayout(export_layout)

        time_export_button = QPushButton("Export time data")
        time_export_button.clicked.connect(lambda: self.connect_export('time'))
        export_layout.addWidget(time_export_button)

        metadata_export_button = QPushButton("Export metadata")
        metadata_export_button.clicked.connect(lambda: self.connect_export('metadata'))
        export_layout.addWidget(metadata_export_button)

        sequence_export_button = QPushButton("Export sequence report")
        sequence_export_button.clicked.connect(lambda: self.connect_export('sequence'))
        export_layout.addWidget(sequence_export_button)

        inner_layout.addWidget(export_group_box)

        inner_layout.addWidget(QLabel("Status: "))
        inner_layout.addWidget(self.text_box)

        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        inner_layout.addWidget(self.pbar)
        # endregion

    def connect_export(self, opt):
        save_as = QFileDialog(self).getSaveFileName(filter="*.csv")[0]

        if save_as:
            if opt == 'time':
                status = scanner.time_report(save_as)
            elif opt == 'metadata':
                status = scanner.metadata_report(save_as)
            elif opt == 'sequence':
                status = scanner.sequence_report(save_as)
            else:
                status = ""

            self.add_to_textbox(status)

    def connect_options(self):
        # self.pbar.setMaximum(len(self.directories))
        # self.worker = ScanWorker(self.preprocess_options, self.directories)
        # len_files = len(list(self.files))
        # self.pbar.setMaximum(len_files)
        self.worker = ScanWorker(self.preprocess_options, self.folder_path)

        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.status_message.connect(self.add_to_textbox)
        self.worker.pbar_value.connect(self.pbar.setValue)

        self.thread.start()

        # Final resets
        self.preprocess_button.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.preprocess_button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.add_to_textbox("Scan complete")
        )
        
    # def run(self):
    #     opts_for_logger = [opt.isChecked() for opt in self.preprocess_options.values()]
    #     logging.info(f"Running scanner with {opts_for_logger}")
    #
    #     if self.preprocess_options['organize_data'].isChecked():
    #         scanner.run_organize_data("", "", parent_widget=self)
    #     if self.preprocess_options['metadata_sequence_scan'].isChecked():
    #         scanner.run_metadata_sequence_scan(self.directories, parent_widget=self)

    def add_to_textbox(self, text, color=None):
        if color:
            self.status_text += f"<p><font color={color}> {text} </font></p>"
        else:
            self.status_text += f"<p> {text} </p>"
        self.text_box.setHtml(self.status_text)
