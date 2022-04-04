import sys
from PyQt5.QtWidgets import QMessageBox


class MessageBox:
    is_gui = False if len(sys.argv) > 1 else True

    @classmethod
    def msg_box_warning(cls, error_text, **kwargs):
        if cls.is_gui:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setText(error_text)

            if 'info' in kwargs:
                msg.setInformativeText(kwargs['info'])
            if 'details' in kwargs:
                msg.setDetailedText(kwargs['details'])

            msg.setStandardButtons(QMessageBox.Close)

            msg.exec()
        else:
            print(error_text)

    @classmethod
    def msg_box_info(cls, info_text, **kwargs):
        if cls.is_gui:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
            msg.setText(info_text)

            if 'info' in kwargs:
                msg.setInformativeText(kwargs['info'])
            if 'details' in kwargs:
                msg.setDetailedText(kwargs['details'])

            msg.setStandardButtons(QMessageBox.Close)

            msg.exec()
        else:
            print(info_text)
