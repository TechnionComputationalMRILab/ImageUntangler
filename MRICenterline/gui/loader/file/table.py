from PyQt5.QtWidgets import QTableWidget

import logging
logging.getLogger(__name__)


class FileOpenTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
