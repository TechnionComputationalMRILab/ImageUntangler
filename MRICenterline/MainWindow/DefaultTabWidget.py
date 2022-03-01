from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout


class DefaultTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._grid_layout = QGridLayout(self)

        self.set_up_main_layout()
        self.add_bottom_buttons()

    def set_up_main_layout(self):
        self._grid_layout.setRowStretch(0, 2)
        self._grid_layout.setRowStretch(1, 1)
        self._grid_layout.setRowStretch(2, 1)
        self._grid_layout.setRowStretch(3, 1)
        self._grid_layout.setRowStretch(4, 2)

        self._grid_layout.setColumnStretch(0, 1)
        self._grid_layout.setColumnStretch(1, 2)
        self._grid_layout.setColumnStretch(2, 1)

        self.add_mri_images_button = QPushButton("Open MRI Images")
        self.add_mri_images_button.setMinimumSize(600, 300)
        self._grid_layout.addWidget(self.add_mri_images_button, 1, 1, 1, 1)

    def add_bottom_buttons(self):
        self._bottom_layout = QHBoxLayout()

        self.preferences_button = QPushButton("Preferences")
        self.preferences_button.setMinimumSize(200, 300)
        self._bottom_layout.addWidget(self.preferences_button)

        self.scan_folders_button = QPushButton("Pre-process Folders")
        self.scan_folders_button.setMinimumSize(200, 300)
        self._bottom_layout.addWidget(self.scan_folders_button)

        self.load_from_json_button = QPushButton("Load Annotations")
        self.load_from_json_button.setMinimumSize(200, 300)
        self._bottom_layout.addWidget(self.load_from_json_button)

        self._grid_layout.addLayout(self._bottom_layout, 2, 1, 1, 1)

        self.open_from_folder = QPushButton("Open single MRI image from folder")
        self.open_from_folder.setMinimumSize(600, 100)
        self._grid_layout.addWidget(self.open_from_folder, 3, 1, 1, 1)

    def connect_add_mri_images_button(self, func):
        self.add_mri_images_button.clicked.connect(func)

    def connect_preferences_button(self, func):
        self.preferences_button.clicked.connect(func)

    def connect_scan_folders_button(self, func):
        self.scan_folders_button.clicked.connect(func)

    def connect_load_from_json_button(self, func):
        self.load_from_json_button.clicked.connect(func)

    def connect_open_mri_from_folder_button(self, func):
        self.open_from_folder.clicked.connect(func)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = DefaultTabWidget()
    win.showMaximized()
    win.show()
    sys.exit(app.exec())
