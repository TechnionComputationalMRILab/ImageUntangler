__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

from MRICenterline.MainWindow import App
from MRICenterline.Config.initial_config import Config
from PyQt5.QtWidgets import QApplication
from sys import exit


from icecream import ic, install
install()
ic.configureOutput(includeContext=True)


if __name__ == "__main__":
    conf = Config()
    app = QApplication([])

    MainWindow = App(initial_run=conf.is_first_run)
    MainWindow.show()
    exit(app.exec_())
