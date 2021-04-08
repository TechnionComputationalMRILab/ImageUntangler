import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from MPRWindow2.MPRW_Control import MPRW_Control
from MPRWindow2.MPRW_View import MPRW_View


sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.set_icon()
        self.set_title()
        self.setStyleSheet(stylesheets.get_sheet_by_name("Default"))

        self._control_is_set = False
        self.control = None

    def set_control(self, control: MPRW_Control):
        self.control = control
        self.view = MPRW_View(self.control)
        self._control_is_set = True

    def open_(self):
        if self._control_is_set:
            self._set_up_layout()
        else:
            raise LookupError("No data passed to MPR Window!")

    def _set_up_layout(self):
        self.setMinimumSize(QSize(1920, 1080))
        QBtn = QDialogButtonBox.Help | QDialogButtonBox.Close

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.helpRequested.connect(lambda: self._help_button())
        self.buttonBox.rejected.connect(lambda: self._close_button())

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view.MPRW_Top)
        self.layout.addWidget(self.view.MPRW_Bottom)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec()

    def set_title(self):
        self.setWindowTitle(config_data.get_config_value("AppName") + ': MPR Window')

    def set_icon(self):
        self.setWindowIcon(QIcon(config_data.get_icon_file_path()))

    def _close_button(self):
        print("close clicked")
        pass

    def _help_button(self):
        print("aaa")
        pass
