from PyQt5.QtWidgets import QStatusBar, QProgressBar


class DisplayPanelStatus(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.showMessage("Ready", 3000)
