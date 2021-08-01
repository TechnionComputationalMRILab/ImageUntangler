from PyQt5.QtWidgets import QDockWidget
from PyQt5.Qt import QCloseEvent

from MRICenterline.CenterlinePanel.Model.CenterlineModel import CenterlineModel
from MRICenterline.Interface import DisplayCenterlineInterface

import logging
logging.getLogger(__name__)


class CenterlinePanel(QDockWidget):
    def __init__(self, image, interface, parent):
        super().__init__(parent)
        logging.info("Initializing CenterlinePanel")

        self.setWindowTitle("centerline panel")

        self.model = CenterlineModel(image, interface)
        self.setWidget(self.model.view)
        self.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        logging.info("Centerline Panel closed")
