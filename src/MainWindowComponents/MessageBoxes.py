from PyQt5.QtWidgets import QMessageBox


def invalidDirectoryMessage():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet("QLabel{min-width:300 px; min-height: 200 px; font-size: 24px;} QPushButton{ width:250px; font-size: 18px; }");
    errorMessage.setWindowTitle("Invalid Directory")
    errorMessage.setText("Selected Directory has No MRI Images")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.exec_()