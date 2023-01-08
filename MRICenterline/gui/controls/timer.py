from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
import qtawesome as qta
from MRICenterline.gui.display.toolbar_connect import timer_status


class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.model = None

        self.start_button = QPushButton(qta.icon('mdi.timer-off-outline'), "Start timer")
        self.stop_button = QPushButton("Stop timer")
        self.pause_button = QPushButton("Pause timer")
        self.resume_button = QPushButton("Resume timer")

        self.stop_button.hide()
        self.pause_button.hide()
        self.resume_button.hide()

        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.resume_button.clicked.connect(self.resume_timer)

        self.layout.addWidget(self.start_button, 0, 0, 1, 2)
        self.layout.addWidget(self.stop_button, 0, 0, 1, 1)

        self.layout.addWidget(self.pause_button, 0, 1, 1, 1)
        self.layout.addWidget(self.resume_button, 0, 1, 1, 1)

    def attach_model(self, model):
        self.model = model

    def reset(self):
        self.start_button.show()
        self.stop_button.hide()
        self.pause_button.hide()
        self.resume_button.hide()

    def start_timer(self):
        self.start_button.hide()
        self.stop_button.show()
        self.pause_button.show()

        if self.model:
            timer_status(self.model, "START")

    def stop_timer(self):
        self.stop_button.hide()
        self.pause_button.hide()
        self.resume_button.hide()
        self.start_button.show()

        if self.model:
            timer_status(self.model, "STOP")

    def pause_timer(self):
        self.pause_button.hide()
        self.resume_button.show()

        if self.model:
            timer_status(self.model, "PAUSE")

    def resume_timer(self):
        self.resume_button.hide()
        self.pause_button.show()

        if self.model:
            timer_status(self.model, "RESUME")
