from PyQt5.QtCore import QObject, pyqtSignal
from MRICenterline.app.database.dicompiler_sqlite import SQLiteDatabase

import logging
logging.getLogger(__name__)


class ScanWorker(QObject):
    finished = pyqtSignal()
    status_message = pyqtSignal(str)
    pbar_value = pyqtSignal(int)

    def __init__(self, options, directory, parent=None):
        super().__init__(parent)
        self.options = options
        self.directory = directory

    def run(self):
        opts_for_logger = [opt.isChecked() for opt in self.options.values()]
        logging.info(f"Running scanner with {opts_for_logger}")

        if self.options['organize_data'].isChecked():
            # scanner.run_organize_data("", "", parent_widget=self)
            self.status_message.emit("Not implemented")
        if self.options['metadata_sequence_scan'].isChecked():
            # for index, folder in enumerate(self.directories):
            #     output = scanner.get_metadata(folder, index, num_folders, None)
            #     self.status_message.emit(f"[{1 + index} / {num_folders}] Reading {folder}")
            #     self.status_message.emit(f'{output}')
            #     self.pbar_value.emit(index + 1)

            sqlite_db = SQLiteDatabase(self.directory, verbose=True, pbar=True)
            sqlite_db.generate_sqlite(fr"{self.directory}\metadata.db")


            # f = io.StringIO()
            # with redirect_stdout(f):
            #     db = Database(self.directory, skip_initial_scan=True, verbose=True)
            #     db.scan_dicom()
            # self.status_message.emit(f'{f}')

            # for index, file in enumerate(self.files):
            #     pass


        self.finished.emit()


