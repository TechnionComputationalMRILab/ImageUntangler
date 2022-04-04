from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QShortcut
from PyQt5.QtGui import QKeySequence
import qtawesome as qta

from MRICenterline.gui.splash import connect


class IUInitialWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        grid_layout.setRowStretch(0, 2)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setRowStretch(3, 2)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 2)
        grid_layout.setColumnStretch(2, 1)

        add_mri_images_button = QPushButton("Open MRI Images")
        add_mri_images_button.setIcon(qta.icon('ei.file-new'))
        add_mri_images_button.setMinimumSize(600, 300)
        add_mri_images_button.clicked.connect(lambda: connect.custom_open(self))
        grid_layout.addWidget(add_mri_images_button, 1, 1, 1, 1)

        # self.add_bottom_buttons()
        bottom_layout = QHBoxLayout()

        preferences_button = QPushButton("Preferences")
        preferences_button.setIcon(qta.icon('fa.gear'))
        preferences_button.setMinimumSize(200, 300)
        preferences_button.clicked.connect(lambda: connect.show_preferences_dialog(self))

        bottom_layout.addWidget(preferences_button)

        scan_folders_button = QPushButton("Pre-process Folders")
        scan_folders_button.setIcon(qta.icon('mdi.magnify-scan'))
        scan_folders_button.setMinimumSize(200, 300)
        scan_folders_button.clicked.connect(lambda: connect.bulk_scanner(self))
        bottom_layout.addWidget(scan_folders_button)

        load_from_json_button = QPushButton("Load Annotations")
        load_from_json_button.setIcon(qta.icon('fa.folder-open-o'))
        load_from_json_button.setMinimumSize(200, 300)
        load_from_json_button.clicked.connect(lambda: connect.load_previous_annotation(self))
        bottom_layout.addWidget(load_from_json_button)

        grid_layout.addLayout(bottom_layout, 2, 1, 1, 1)

        ########################################
        #             "cheat codes"            #
        ########################################
        open_using_file_dialog = QShortcut(QKeySequence('Ctrl+q'), self)
        open_using_file_dialog.activated.connect(lambda: connect.open_using_file_dialog(self))

