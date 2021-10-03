import csv
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QVBoxLayout, QLabel, \
                            QGridLayout, QTextEdit, QFileDialog, QHBoxLayout, QCheckBox

from . import Scanner
from MRICenterline.Config import ConfigParserRead as CFG

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
        _preprocess_options = {
            "move_dicom":
                QCheckBox("Move DICOM files to destination (delete original)"),
            "rename_folders":
                QCheckBox("Rename folders to 1, 2, 3..."),
            "seqdict":
                QCheckBox("Generate sequence directory"),
            "report":
                QCheckBox("Generate folder report as CSV")
        }

        _preprocess_options['move_dicom'].setChecked(False)
        _preprocess_options['move_dicom'].setEnabled(False)

        _preprocess_options['rename_folders'].setChecked(True)
        _preprocess_options['seqdict'].setChecked(True)
        _preprocess_options['report'].setChecked(True)

        _preprocess_options_layout = QHBoxLayout()
        [_preprocess_options_layout.addWidget(chkbox) for chkbox in _preprocess_options.values()]

        _preprocess_button = QPushButton("Start")
        _preprocess_button.setStatusTip("Generates sequence dictionary + folder report")
        _preprocess_button.setMinimumSize(600, 100)

        if _preprocess_options['move_dicom'].isChecked():
            _preprocess_button.clicked.connect(self.copy_files)
            _preprocess_button.clicked.connect(self.delete_original_folder)
        else:
            _preprocess_button.clicked.connect(self.copy_files)

        if _preprocess_options['rename_folders'].isChecked():
            _preprocess_button.clicked.connect(self.rename_folders)
        if _preprocess_options['seqdict'].isChecked():
            _preprocess_button.clicked.connect(self.generate_seqdict)
        if _preprocess_options['report'].isChecked():
            _preprocess_button.clicked.connect(self.generate_report)

        self._v_layout.addWidget(_preprocess_button)
        self._v_layout.addLayout(_preprocess_options_layout)

    def generate_seqdict(self):
        logging.info("Starting folder scan for seqdict")

        for i, val in enumerate(self.directories):
            Scanner.generate_seq_dict(val)
            self._add_to_textbox(f"<b>[Folder {i+1}/{len(self.directories)}]</b>: {val}")

            if len(self.directories) > 1:
                self.prog_bar.setValue(i)

        self._add_to_textbox("Done! You can close this tab now", color='blue')

    def generate_report(self):
        logging.info("Starting folder scan for reporting")

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

            _csv_filename, _ = QFileDialog.getSaveFileName(self, "Save report to",
                                                           CFG.get_config_data("folders", 'default-save-to-folder'),
                                                           "%s Files (*.%s);;All Files (*)" % ("csv".upper(), "csv"))

            if _csv_filename:
                logging.debug(f"Saving report to {_csv_filename}")

                with open(_csv_filename, 'w', encoding='utf8', newline='') as output_file:
                    fc = csv.DictWriter(output_file, fieldnames=_to_csv[0].keys())
                    fc.writeheader()
                    fc.writerows(_to_csv)

                self._add_to_textbox(f"Done! Report is saved to {_csv_filename}. You can close this tab now",
                                     color='blue')

    def rename_folders(self):
        self._add_to_textbox("Renaming the folders...")
        pass

    def copy_files(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Select destination",
                                                  CFG.get_config_data("folders", 'default-save-to-folder'))

        if fileName:
            logging.info(f"Copying the dicom files to {fileName}")
            self._add_to_textbox(f"Copying the dicom files to {fileName}")
        pass

    def delete_original_folder(self):
        pass

    def _add_to_textbox(self, text, color=None):
        if color:
            self.status_text += f"<p><font color={color}> {text} </font></p>"
        else:
            self.status_text += f"<p> {text} </p>"
        self.text_box.setHtml(self.status_text)
