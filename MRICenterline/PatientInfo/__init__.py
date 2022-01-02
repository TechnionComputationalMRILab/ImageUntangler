import os

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTextEdit, QDialog, QDialogButtonBox, QPushButton

from MRICenterline.PatientInfo.PatientTable import PatientTable
from MRICenterline.PatientInfo.CommentText import CommentParser

import logging
logging.getLogger(__name__)


class PatientInfoPanel(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.data_folder = os.path.join(parent.images.dicom_list[0].get_folder(), "data")
        self._comment_parser = CommentParser(parent=self)
        self.unsaved_text = ""
        self._set_up_widgets()

        if parent.current_sequence == -1:
            # current view is loaded from json file
            self.current_sequence = -1
        else:
            self.current_sequence = parent.images.get_sequences()[parent.current_sequence]

    def _set_up_widgets(self):
        self._table = PatientTable(parent=self)

        self._comment_box = QTextEdit()
        self._set_comment_box_text()

        self._v_layout = QVBoxLayout(self)
        # self._v_layout.addWidget(self._table)
        self._v_layout.addWidget(self._comment_box)

        _button_layout = QHBoxLayout()

        self._buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        if not self._comment_parser.is_empty:
            self._load_previous = QPushButton("Show Previous Comments")
            self._load_previous.setCheckable(True)
            self._load_previous.setChecked(True)
            _button_layout.addWidget(self._load_previous)
            self._load_previous.clicked.connect(self._show_previous_comments)

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        _button_layout.addWidget(self._buttons)

        self._v_layout.addLayout(_button_layout)
        # self._v_layout.addWidget(self._buttons)

    def _set_comment_box_text(self):
        logging.info("Setting comment box text")

        # if self.current_sequence == -1:
        #     self._comment_box.setHtml('NOT SUPPORTED')

        if self._comment_parser.is_empty:
            self._comment_box.setPlaceholderText("No previous comments found")
        else:
            self._comment_box.setPlaceholderText("Previous comments found. Click button below to load")

    def _show_previous_comments(self):
        if not self._load_previous.isChecked():
            logging.info("Showing previous comments")
            self.unsaved_text = self._comment_box.toPlainText()

            self._comment_box.setReadOnly(True)
            self._comment_box.clear()
            self._comment_box.setText(self._comment_parser.comment_text)

            self._load_previous.setChecked(False)
            self._load_previous.setText("Add comments")
        else:
            logging.info("Setting comment box to editable")
            self._comment_box.setReadOnly(False)
            self._comment_box.clear()

            if self.unsaved_text:
                self._comment_box.setText(self.unsaved_text)
            else:
                self._comment_box.setPlaceholderText("Previous comments found. Click button below to load")

            self._load_previous.setChecked(True)
            self._load_previous.setText("Show Previous Comments")

    def accept(self) -> None:
        input_text = self._comment_box.toPlainText()
        self._comment_parser.save_comments(input_text)

        super(PatientInfoPanel, self).accept()
