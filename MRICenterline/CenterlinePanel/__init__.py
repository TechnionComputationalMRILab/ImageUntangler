from PyQt5.QtGui import *
from PyQt5.Qt import *

from MRICenterline.CenterlinePanel.Model.CenterlineModel import CenterlineModel
from MRICenterline.Interface import DisplayCenterlineInterface

import logging
logging.getLogger(__name__)


class CenterlinePanel(QDockWidget):
    def __init__(self, image, interface, parent):
        super().__init__(parent)

        self.setWindowTitle("centerline panel")
        self.allowedAreas = Qt.BottomDockWidgetArea

        self.model = CenterlineModel(image, interface)
        self.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        logging.info("Centerline Panel closed")
