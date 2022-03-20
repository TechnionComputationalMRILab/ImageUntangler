import csv
import os
import shutil
from pathlib import Path
from glob import glob
from copy import deepcopy
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QVBoxLayout, QLabel, \
                            QGridLayout, QTextEdit, QFileDialog, QGroupBox, QCheckBox

from . import Scanner

import logging
logging.getLogger(__name__)


class ProgressWidget(QWidget):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)

        self.folder_path = folder_path
        self.directories = Scanner.get_directories(self.folder_path)
        self.directories.remove(Path(self.folder_path))
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

        self.text_box = QTextEdit()
        self.text_box.setHtml(self.status_text)
        self._add_to_textbox("<b>Does not currently support sequences with different patients in the same "
                             "directory.</b>", color='red')

        self._v_layout.addWidget(_warning)
        self._v_layout.addWidget(self.text_box)

        self._run_preprocessing()

        if len(self.directories) > 1:
            self.prog_bar = QProgressBar(self)
            self.prog_bar.setMaximum(len(self.directories) - 1)
            self._v_layout.addWidget(self.prog_bar)

        self._grid_layout.addLayout(self._v_layout, 1, 1, 1, 1)

    def _run_preprocessing(self):
        self._preprocess_options = {
            "move_dicom":
                QCheckBox("Move DICOM files to destination (delete original)"),
            "rename_folders":
                QCheckBox("Rename folders to 1, 2, 3..."),
            "seqdict":
                QCheckBox("Generate sequence directory"),
            "report":
                QCheckBox("Generate folder metadata report"),
            "directory":
                QCheckBox("Generate time/directory report"),
            "time_report":
                QCheckBox("Generate report on timer data as CSV"),
            "rebuild_directory":
                QCheckBox("Rebuild the data directory file (re-initialize folder, ignores all flags)"),
            "initialize_new_case_folder":
                QCheckBox("Initialize new case folder (ignores all flags)")
        }

        self._preprocess_options['move_dicom'].setChecked(False)
        self._preprocess_options['move_dicom'].setEnabled(False)
        self._preprocess_options['rename_folders'].setChecked(False)
        self._preprocess_options['rename_folders'].setEnabled(False)

        self._preprocess_options['seqdict'].setChecked(True)
        self._preprocess_options['report'].setChecked(True)
        self._preprocess_options['directory'].setChecked(True)

        _preprocess_options_group_box = QGroupBox("Options")
        _preprocess_options_layout = QGridLayout()
        _preprocess_options_group_box.setLayout(_preprocess_options_layout)

        _preprocess_options_layout.addWidget(self._preprocess_options['seqdict'], 0, 0)
        _preprocess_options_layout.addWidget(self._preprocess_options['report'], 1, 0)
        _preprocess_options_layout.addWidget(self._preprocess_options['rename_folders'], 0, 1)
        _preprocess_options_layout.addWidget(self._preprocess_options['move_dicom'], 1, 1)
        _preprocess_options_layout.addWidget(self._preprocess_options['time_report'], 2, 0)
        _preprocess_options_layout.addWidget(self._preprocess_options['rebuild_directory'], 3, 1)
        _preprocess_options_layout.addWidget(self._preprocess_options['directory'], 3, 0)
        _preprocess_options_layout.addWidget(self._preprocess_options['initialize_new_case_folder'], 2, 1)

        _preprocess_button = QPushButton("Start")
        _preprocess_button.setStatusTip("Generates sequence dictionary + folder report")
        _preprocess_button.setMinimumSize(600, 100)

        _preprocess_button.clicked.connect(self._connect_options)

        self._v_layout.addWidget(_preprocess_button)
        # self._v_layout.addLayout(_preprocess_options_layout)
        self._v_layout.addWidget(_preprocess_options_group_box)

    def _connect_options(self):
        _opts_for_logger = [opt.isChecked() for opt in self._preprocess_options.values()]
        logging.info(f"Running scanner with {_opts_for_logger}")

        if self._preprocess_options['rebuild_directory'].isChecked():
            self._rebuild_data_directory()
            return

        if self._preprocess_options['initialize_new_case_folder'].isChecked():
            self._initialize_new_folder()
            return

        if self._preprocess_options['seqdict'].isChecked():
            self._generate_seqdict()
        if self._preprocess_options['report'].isChecked():
            self._generate_metadata_report()
        if self._preprocess_options['time_report'].isChecked():
            self._generate_time_report()
        if self._preprocess_options['directory'].isChecked():
            self._generate_directory_report()

    def _generate_directory_report(self, get_only_latest=True, also_show_centerline=False):
        logging.info("Scanning for data directories for the directory CSV")

        _to_csv = Scanner.generate_directory_report(self.folder_path, get_only_latest, also_show_centerline)

        logging.debug(f'writing to file: {_to_csv}')
        with open(os.path.join(self.folder_path, 'directory.csv'), 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=_to_csv[0].keys())
            fc.writeheader()
            fc.writerows(_to_csv)

        self._add_to_textbox(f"Done! Report is saved to {os.path.join(self.folder_path, 'generated directory.csv')}. "
                             f"You can close this tab now",
                             color='blue')

    def _generate_time_report(self):
        logging.info("Scanning for data directories for the time report")

        # go through all the data directories
        _to_csv = Scanner.generate_time_report(self.folder_path)

        with open(os.path.join(self.folder_path, 'time report.csv'), 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=_to_csv[0].keys())
            fc.writeheader()
            fc.writerows(_to_csv)

        self._add_to_textbox(f"Done! Report is saved to {os.path.join(self.folder_path, 'time report.csv')}. "
                             f"You can close this tab now",
                             color='blue')

    def _generate_seqdict(self):
        logging.info("Starting folder scan for seqdicts")

        for i, val in enumerate(self.directories):
            Scanner.generate_seq_dict(val)
            self._add_to_textbox(f"<b>[Folder {i+1}/{len(self.directories)}]</b>: {val}")

            if len(self.directories) > 1:
                self.prog_bar.setValue(i)

        self._add_to_textbox("Done! You can close this tab now", color='blue')

    def _generate_metadata_report(self):
        """
        creates a report.csv with metadata on the folders, sequence names, etc
        """
        logging.info("Starting folder scan for metadata reporting")

        try:
            os.remove(os.path.join(self.folder_path, 'report.csv'))
        except Exception:
            pass

        if len(self.directories) > 0:
            self._add_to_textbox("Starting scan!")

            _to_csv = []
            for i, val in enumerate(self.directories):
                _dict = Scanner.generate_report(val)
                if _dict:
                    _dict['Path'] = val
                    _to_csv.append(_dict)
                else:
                    pass

                self._add_to_textbox(f"<b>[Folder {i+1}/{len(self.directories)}]</b>: {val}")

                if len(self.directories) > 1:
                    self.prog_bar.setValue(i)

            logging.debug(f"Saving report")

            with open(os.path.join(self.folder_path, 'report.csv'), 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, fieldnames=_to_csv[0].keys())
                fc.writeheader()
                fc.writerows(_to_csv)

        # json_files = [Path(file) for file in glob(f"{self.folder_path}/**/seqdict.json", recursive=True)]
        # if json_files:
        #     [os.remove(file) for file in json_files]
        #
        # data_dirs = [Path(file) for file in glob(f"{self.folder_path}/**/data/", recursive=True)]
        # if data_dirs:
        #     [os.rmdir(file) for file in data_dirs]

            self._add_to_textbox(f"Done! Report is saved to {os.path.join(self.folder_path, 'report.csv')}. "
                                 f"You can close this tab now",
                                 color='blue')

    def _rename_folders(self):
        self._add_to_textbox("Renaming folders is not yet implemented", color='blue')

    def _copy_files(self):
        self._add_to_textbox("Copying files is not yet implemented", color='blue')
        # fileName, _ = QFileDialog.getSaveFileName(self, "Select destination")
        #
        # if fileName:
        #     logging.info(f"Copying the dicom files to {fileName}")
        #     self._add_to_textbox(f"Copying the dicom files to {fileName}")

    def _rebuild_data_directory(self):
        self._add_to_textbox("Rebuilding data directories...", color='blue')

        # clear the csv files
        try:
            os.remove(os.path.join(self.folder_path, 'report.csv'))
        except Exception:
            self._add_to_textbox("metadata report not found")
        else:
            self._add_to_textbox(f"Removing report.csv")

        try:
            os.remove(os.path.join(self.folder_path, 'directory.csv'))
        except Exception:
            self._add_to_textbox("annotation directory not found")
        else:
            self._add_to_textbox("Removing directory.csv")

        # delete these
        bad_data_folders = [Path(file) for file in glob(f'{self.folder_path}/*/data/data/')]
        for i in bad_data_folders:
            shutil.rmtree(i)
            self._add_to_textbox(f'Removing bad data folder: {i}')

        # keep these
        annotation_cl = [Path(file) for file in glob(f"{self.folder_path}/*/data/*.centerline.annotation.json")]
        annotation_main = [Path(file) for file in glob(f"{self.folder_path}/*/data/*.annotation.json")]
        all_files_in_data_dir = [Path(file) for file in glob(f"{self.folder_path}/*/data/*")]
        to_delete = [value for value in all_files_in_data_dir if value not in annotation_cl + annotation_main]

        for i in to_delete:
            os.remove(i)
            self._add_to_textbox(f'Removing {i}')

        self._add_to_textbox("Generating sequence dictionaries", color='blue')
        self._generate_seqdict()

        self._add_to_textbox("Generating folder metadata reports", color='blue')
        self._generate_metadata_report()

        self._add_to_textbox("Generating annotation directory", color='blue')
        self._generate_directory_report()

    def _initialize_new_folder(self):
        pass

    def _delete_original_folder(self):
        raise NotImplementedError

    def _add_to_textbox(self, text, color=None):
        if color:
            self.status_text += f"<p><font color={color}> {text} </font></p>"
        else:
            self.status_text += f"<p> {text} </p>"
        self.text_box.setHtml(self.status_text)