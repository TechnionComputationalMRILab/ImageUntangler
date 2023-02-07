from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from pyqtspinner import WaitingSpinner

from MRICenterline.gui.display.toolbar_connect import calculate
from MRICenterline.app.points.status import PointStatus
import time


import logging

logging.getLogger(__name__)


class ShortestPathWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.output = None

    def run(self):
        logging.info("Running shortest path algorithm as worker")

        self.data.fill()
        # calculate(self.model, PointStatus.MPR_FILL)

        self.output = 0

        self.finished.emit()
