import qtawesome as qta
from PyQt5.QtWidgets import QToolBar, QPushButton

from MRICenterline.gui.window import toolbar_connect


class IUToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)

        setting_button = QPushButton(qta.icon('fa.gear'), "Settings")
        setting_button.setFlat(True)
        self.addWidget(setting_button)
        setting_button.clicked.connect(lambda: toolbar_connect.show_preferences_dialog(self))

        help_button = QPushButton(qta.icon('fa5s.info-circle'), "Help")
        help_button.setFlat(True)
        self.addWidget(help_button)
        help_button.clicked.connect(lambda: toolbar_connect.open_help_dialog(self))
