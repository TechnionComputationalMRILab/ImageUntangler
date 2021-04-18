import sys
import os
from PyQt5.Qt import *
from MPRWindow.MPRW_Model import MPRW_Model

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRWindow(QDialog):
    """ dialog box for the mpr window """
    def __init__(self, points, image_data):
        super().__init__()

        self.set_icon()
        self.set_title()
        self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        self.setMinimumSize(QSize(1920, 1080))

        self.model = MPRW_Model(points, image_data)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(lambda: self.model.view.help_button("some help text here"))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.model.view)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.show()

    def set_title(self):
        self.setWindowTitle(config_data.get_config_value("AppName") + ': MPR Window')

    def set_icon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))

    def closeEvent(self, event) -> None:
        print("close event")
