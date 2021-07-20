from PyQt5.QtWidgets import QMessageBox


def msg_box_warning(error_text, **kwargs):
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


def msg_box_info(info_text, **kwargs):
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
