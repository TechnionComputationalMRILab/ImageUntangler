from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
import qtawesome as qta

from MRICenterline.app.points.status import PickerStatus, TimerStatus, PointStatus
from MRICenterline.app.gui_data_handling.centerline_model import CenterlineModel


class CenterlinePanelToolbarButtons(QWidget):
    def __init__(self,
                 model: CenterlineModel,
                 parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
