__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

from MRICenterline.MainWindow import App
from MRICenterline.utils.log import LOGGING_CONFIG
from PyQt5.QtWidgets import QApplication
from sys import exit
import logging.config

#from icecream import ic, install
#install()

# ic.configureOutput(includeContext=True)

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)

    app = QApplication([])
    MainWindow = App()
    MainWindow.show()
    exit(app.exec_())
