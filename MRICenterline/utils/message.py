from PyQt5.QtWidgets import QMessageBox


def msg_box_error(error_text, **kwargs):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText(error_text)

    if 'info' in kwargs:
        msg.setInformativeText(kwargs['info'])
    if 'details' in kwargs:
        msg.setDetailedText(kwargs['details'])

    msg.setStandardButtons(QMessageBox.Close)
