from PyQt5.Qt import *
from util import logger
lo = logger.get_logger()


class DialogLog(QDialog):
    def __init__(self):
        super(DialogLog, self).__init__()
        lo.debug("Opening log dialog box")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._set_up_textbox()
        self._set_buttons()

        self.resize(QSize(800, 600))
        self.exec()

    def _set_buttons(self):
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self.close)  # TODO: FIX??
        self.layout.addWidget(self.buttonBox)

    def _set_up_textbox(self):
        self.textbox = QPlainTextEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText(logger.get_log_stream())
        self.layout.addWidget(self.textbox)

    def closeEvent(self, a0: QCloseEvent) -> None:
        pass
