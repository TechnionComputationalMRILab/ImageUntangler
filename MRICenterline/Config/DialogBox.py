from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class DialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Preferences")

        _buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel | \
                   QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Help

        self.button_box = QDialogButtonBox(_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.helpRequested.connect(self.help)
        # self.button_box.setOrientation(Qt.Vertical)

        self.layout = QVBoxLayout()
        self.layout.addWidget(PreferencesWidget(self))
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.setMinimumWidth(1000)

        self.exec() # exec, not show, so that dialog box is application modal

    def accept(self) -> None:
        print('ok')
        super().accept()

    def reject(self) -> None:
        print("cancel")
        super().reject()

    def help(self):
        print("help")


class PreferencesWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.categories = QListWidget()
        self.categories.insertItem(0, "Folders")
        self.categories.insertItem(1, 'Display')
        self.categories.insertItem(2, "Length style")
        self.categories.insertItem(3, "Centerline style")
        self.categories.insertItem(4, "Testing")
        self.categories.currentRowChanged.connect(self.current_category_changed)
        self.categories.setMaximumWidth(200)

        self.main_layout = QHBoxLayout()

        self.preferences = QStackedWidget(self)
        self.preferences.addWidget(self.folders())
        self.preferences.addWidget(self.display())
        self.preferences.addWidget(self.length_display_style())

        self.main_layout.addWidget(self.categories, stretch=1)
        self.main_layout.addWidget(self.preferences, stretch=3)
        self.setLayout(self.main_layout)

    def current_category_changed(self, i):
        self.preferences.setCurrentIndex(i)

    def folders(self):
        _folders_widget = QWidget()
        _folders_layout = QFormLayout()

        _folders_widget.setLayout(_folders_layout)
        self.default_folder = QLineEdit(CFG.get_config_data('folders', 'default-folder'))

        _folders_layout.addRow(QLabel("Add MRI Images default folder"), self.default_folder)
        _folders_layout.addRow(QLabel("Save annotation to"), self.default_save_to_folder)

        return _folders_widget

    def display(self):
        _display_widget = QWidget()
        _display_layout = QFormLayout()

        _display_widget.setLayout(_display_layout)
        self.start_maximized = QCheckBox()

        _display_layout.addRow(QLabel("Start maximized"), self.start_maximized)

        return _display_widget

    def length_display_style(self):
        _length_widget = QWidget()
        _length_layout = QFormLayout()

        _length_widget.setLayout(_length_layout)

        _length_color_button = QPushButton("Select")
        _length_color_button.clicked.connect(self.get_color)

        _length_layout.addRow(QLabel("Color"), _length_color_button)
        _length_layout.addRow(QLabel("Marker size"))
        _length_layout.addRow(QLabel("Marker type"))
        _length_layout.addRow(QLabel("Line thickness"))
        _length_layout.addRow(QLabel("Line style"))
        _length_layout.addRow(QLabel("Measurement style"))

        return _length_widget

    def get_color(self):
        self._length_color = QColorDialog.getColor()
        print(str(self._length_color.getRgb()))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = DialogBox()
    sys.exit(app.exec())
