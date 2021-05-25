from PyQt5.Qt import *
from MPRWindow.Model import MPRW_Model

from util import config_data, stylesheets, logger
logger = logger.get_logger()


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
        self.setWindowTitle('MPR Window')

    def set_icon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))

    def closeEvent(self, event) -> None:
        logger.debug("Closing MPR Window Dialogbox")
        print("close event")
