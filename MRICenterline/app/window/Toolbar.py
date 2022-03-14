import qtawesome as qta
from PyQt5.QtWidgets import QToolBar, QPushButton

from . import connect


class IUToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)

        button = QPushButton("Open new MRI case")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda : print("test"))
        button.setIcon(qta.icon('ei.file-new'))

        button = QPushButton("Load from previous")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda : print("test"))
        button.setIcon(qta.icon('fa.folder-open-o'))

        button = QPushButton("Bulk scanner")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda: print("test"))
        button.setIcon(qta.icon('mdi.magnify-scan'))

        button = QPushButton("Settings")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda: connect.show_preferences_dialog(self))
        button.setIcon(qta.icon('fa.gear'))

        button = QPushButton("Help")
        button.setFlat(True)
        self.addWidget(button)
        button.clicked.connect(lambda: print("test"))
        button.setIcon(qta.icon('fa5s.info-circle'))
