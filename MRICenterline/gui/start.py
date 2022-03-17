from sys import exit
from PyQt5.QtWidgets import QApplication

from MRICenterline.gui.window.MainWindow import IUMainWindow


def start():
    app = QApplication([])
    main_window = IUMainWindow()
    main_window.show()
    exit(app.exec_())
