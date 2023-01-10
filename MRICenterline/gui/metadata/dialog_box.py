from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5.Qt import Qt

from MRICenterline import CFG

import logging

from MRICenterline.app.gui_data_handling.case_model import CaseModel

logging.getLogger(__name__)


class MetadataDialogBox(QDialog):
    def __init__(self, model: CaseModel, parent=None):
        super().__init__(parent)

        self.sequence_manager = model.sequence_manager
        self.metadata_dict = model.image.get_metadata()
        self.metadata_dict.pop("case_id")

        layout = QVBoxLayout(self)
        label = QLabel(self.clean_text())
        layout.addWidget(label)

    def clean_text(self) -> str:
        lines = ["Information \n\n", " --Patient Metadata-- \n"]

        for k, v in self.metadata_dict.items():
            lines.append(f'{k}: {v}')

        lines.append("\n\n --Image Properties-- \n")

        lines.append(f"Orientation: {self.sequence_manager.orientation}")

        return "\n".join(lines)


def show_metadata_dialog(model, parent):
    metadata = MetadataDialogBox(model=model, parent=parent)
    metadata.exec()
