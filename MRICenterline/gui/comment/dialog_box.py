from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout
from PyQt5.Qt import Qt

from MRICenterline import CFG

import logging
logging.getLogger(__name__)


class CommentDialogBox(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model

