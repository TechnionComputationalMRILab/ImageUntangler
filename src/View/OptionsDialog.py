from PyQt5.QtWidgets import *
from util import config_data, stylesheets
import os
import webbrowser


class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._set_defaults()
        self._set_title()

        self._default_folder()
        self._default_save_to_folder()
        self._set_panels()
        self._set_dialog_buttons()
        self._testing_features()

        self._add_widgets()

        self.show()

    def _add_widgets(self):
        # this is where the order comes in
        self.layout.addWidget(self.panel_groupbox)
        self.layout.addWidget(self.default_folder_groupbox)
        self.layout.addWidget(self.default_save_to_folder_groupbox)
        self.layout.addWidget(self.testing_groupbox)
        self.layout.addWidget(self.buttonBox)

    def _testing_features(self):
        self.testing_groupbox = QGroupBox("Features in testing")
        self.testing_groupbox.setCheckable(True)
        self.testing_groupbox.setChecked(False)

        self.testing_layout = QVBoxLayout()
        self.testing_groupbox.setLayout(self.testing_layout)

        self.testing_display_lines = QCheckBox("Draw lines to connect points")
        self.testing_layout.addWidget(self.testing_display_lines)




    def _default_folder(self):
        self.default_folder_groupbox = QGroupBox("Set Working directory")

        self.default_folder_layout = QVBoxLayout()
        self.default_folder_groupbox.setLayout(self.default_folder_layout)

        self.folder_textbox = QLineEdit(self)
        self.default_folder_layout.addWidget(self.folder_textbox)

        self.folder_textbox.setText(config_data.get_config_value('DefaultFolder'))
        self.folder_textbox.setReadOnly(True)

        _browse = QPushButton("Select working directory")
        _open = QPushButton("Open in Explorer")

        _browse.clicked.connect(self._select_working_directory)
        _browse.clicked.connect(lambda: self.folder_textbox.setText(config_data.get_config_value('DefaultFolder')))

        _open.clicked.connect(lambda: webbrowser.open(config_data.get_config_value('DefaultFolder')))

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout()

        self.buttons_widget.setLayout(self.buttons_layout)
        self.buttons_layout.addWidget(_browse)
        self.buttons_layout.addWidget(_open)

        self.default_folder_layout.addWidget(self.buttons_widget)
        # self.layout.addWidget(self.default_folder_groupbox)

    @staticmethod
    def _select_working_directory():
        fileExplorer = QFileDialog(directory=config_data.get_config_value('DefaultFolder'))
        folderPath = str(fileExplorer.getExistingDirectory())
        if os.path.exists(folderPath):  # if user picked a directory, ie did not X-out the window
            config_data.update_default_config_value("DefaultFolder", folderPath)

    def _default_save_to_folder(self):
        self.default_save_to_folder_groupbox = QGroupBox("Set Default directory for saved files")

        self.default_save_to_folder_layout = QVBoxLayout()
        self.default_save_to_folder_groupbox.setLayout(self.default_save_to_folder_layout)

        self.folder_textbox = QLineEdit(self)
        self.default_save_to_folder_layout.addWidget(self.folder_textbox)

        self.folder_textbox.setText(config_data.get_config_value('DefaultSaveToFolder'))
        self.folder_textbox.setReadOnly(True)

        _browse = QPushButton("Select working directory")
        _open = QPushButton("Open in Explorer")

        _browse.clicked.connect(self._select_working_directory)
        _browse.clicked.connect(lambda: self.folder_textbox.setText(config_data.get_config_value('DefaultSaveToFolder')))

        _open.clicked.connect(lambda: webbrowser.open(config_data.get_config_value('DefaultSaveToFolder')))

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout()

        self.buttons_widget.setLayout(self.buttons_layout)
        self.buttons_layout.addWidget(_browse)
        self.buttons_layout.addWidget(_open)

        self.default_save_to_folder_layout.addWidget(self.buttons_widget)
        # self.layout.addWidget(self.default_folder_groupbox)

    @staticmethod
    def _select_save_to_directory():
        fileExplorer = QFileDialog(directory=config_data.get_config_value('Defaults')['DefaultSaveToFolder'])
        folderPath = str(fileExplorer.getExistingDirectory())
        if os.path.exists(folderPath):  # if user picked a directory, ie did not X-out the window
            config_data.update_default_config_value("DefaultSaveToFolder", folderPath)

    def _set_panels(self):
        self.panel_groupbox = QGroupBox("Set number of panels")

        self.panel_groupbox_layout = QGridLayout()
        self.panel_groupbox.setLayout(self.panel_groupbox_layout)
        self.panel_groupbox_layout.addWidget(QLabel("Horizontal"), 1, 1)
        self.panel_groupbox_layout.addWidget(QLabel("Vertical"), 2, 1)

        self.panel_horizontal_spinbox = QDoubleSpinBox()
        self.panel_vertical_spinbox = QDoubleSpinBox()

        self.panel_horizontal_spinbox.setValue(self.panel_number[0])
        self.panel_horizontal_spinbox.setDecimals(0)
        self.panel_vertical_spinbox.setDecimals(0)

        self.panel_groupbox_layout.addWidget(self.panel_horizontal_spinbox, 1, 2)
        self.panel_groupbox_layout.addWidget(self.panel_vertical_spinbox, 2, 2)
        # self.layout.addWidget(self.panel_groupbox)

    def _set_defaults(self):
        self.panel_number = 2, 0

    def _set_title(self):
        self.setWindowTitle("Preferences")

    def _set_dialog_buttons(self):
        self._qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(self._qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # self.layout.addWidget(self.buttonBox)

    def accept(self) -> None:
        if not self._check_panel_count():
            QMessageBox.information(self, "Error", 'Need more than 1 panel!')
        else:
            self.panel_number = self._set_panel_number()
            super().accept()

    def _check_panel_count(self):
        return self.panel_horizontal_spinbox.value() + self.panel_vertical_spinbox.value()

    def _set_panel_number(self):
        return int(self.panel_horizontal_spinbox.value()), int(self.panel_vertical_spinbox.value())
