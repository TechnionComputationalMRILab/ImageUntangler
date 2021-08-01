from PyQt5.QtWidgets import QStatusBar, QProgressBar, QFrame, QLabel
import os
import psutil

from MRICenterline.Config import ConfigParserRead as CFG


class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)


class DisplayPanelStatus(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.process_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

        self.showMessage("Ready", 3000)

        self.memory_usage_label = QLabel(f"Memory usage: {round(self.process_usage, 2)} MB")

        if CFG.get_testing_status('show-memory-usage'):
            self.addPermanentWidget(VLine())
            self.addPermanentWidget(self.memory_usage_label)

    def update_memory_usage(self):
        self.process_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        self.memory_usage_label.setText(f"Memory usage: {round(self.process_usage, 2)} MB")
