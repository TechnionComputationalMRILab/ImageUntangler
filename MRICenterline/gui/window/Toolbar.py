import qtawesome as qta
from PyQt5.QtWidgets import QToolBar, QPushButton

from MRICenterline.gui.window import toolbar_connect


class IUToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)

        button = QPushButton("Settings")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda: toolbar_connect.show_preferences_dialog(self))
        button.setIcon(qta.icon('fa.gear'))

        button = QPushButton("Help")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda: toolbar_connect.open_help_dialog(self))
        button.setIcon(qta.icon('fa5s.info-circle'))
