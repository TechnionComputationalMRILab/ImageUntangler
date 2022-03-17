from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QFileDialog, QPushButton, QLabel

from MRICenterline.app.config.file_check import delete_config_file

from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


class InitialConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_edit_text = "No folder selected"

        self.setWindowTitle("Initial Configuration")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel("Select folder with MRI files"))

        line_edit = QLineEdit()
        line_edit.setText(self.line_edit_text)
        line_edit.setReadOnly(True)
        layout.addWidget(line_edit)

        button = QPushButton("Browse...")
        layout.addWidget(button)

        def open_dialog():
            selected_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

            if selected_dir:
                self.line_edit_text = selected_dir
                line_edit.setText(selected_dir)

        button.clicked.connect(open_dialog)

        layout.addWidget(QLabel("Note: All other options will be set to defaults."))

        dialog_buttons = QDialogButtonBox.Save
        self.button_box = QDialogButtonBox(dialog_buttons)
        layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)

    def accept(self) -> None:
        logging.info(f"Setting the data folder as {self.line_edit_text}")
        CFG.set_config_data('folders', 'data-folder', self.line_edit_text)
        super().accept()

    def reject(self) -> None:
        MSG.msg_box_warning("No folder selected. Program will now close.")
        delete_config_file()
        super().reject()


def ask_for_data_folder(parent) -> None:
    import sys

    icd = InitialConfigDialog(parent)
    icd_value = icd.exec()

    if not icd_value:  # user X'ed out of the dialog box
        sys.exit(0)
