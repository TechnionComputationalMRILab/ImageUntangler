import qtawesome as qta
from PyQt5.QtWidgets import QToolBar, QPushButton

from MRICenterline.gui.window import toolbar_connect
from MRICenterline import CFG


class IUToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)

        new_case_button = QPushButton(qta.icon('fa.gear'), "New Case")
        new_case_button.setFlat(True)
        self.addWidget(new_case_button)
        new_case_button.clicked.connect(parent.open_new_case)

        setting_button = QPushButton(qta.icon('fa.gear'), "Settings")
        setting_button.setFlat(True)
        self.addWidget(setting_button)
        setting_button.clicked.connect(lambda: toolbar_connect.show_preferences_dialog(self))

        help_button = QPushButton(qta.icon('fa5s.info-circle'), "Help")
        help_button.setFlat(True)
        self.addWidget(help_button)
        help_button.clicked.connect(lambda: toolbar_connect.open_help_dialog(self))
        help_button.setEnabled(CFG.get_testing_status(testing=None))  # TODO: populate the help dialog
