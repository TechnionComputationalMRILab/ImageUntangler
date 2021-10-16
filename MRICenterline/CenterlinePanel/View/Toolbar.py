from PyQt5.QtWidgets import QWidget, QToolBar, QSizePolicy
from PyQt5.Qt import Qt

from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class CenterlinePanelToolbar(QToolBar):
    def __init__(self, parent, manager):
        super().__init__(parent=parent)
        logging.debug("Initializing toolbar")
        self.set_toolbar_display_style()
        self.manager = manager
        self.control = self.manager.control

        self.set_up_toolbar_order()

    def set_toolbar_display_style(self):
        if CFG.get_config_data('display', 'toolbar-style') == 'icon':
            pass
        elif CFG.get_config_data('display', 'toolbar-style') == 'text':
            pass
        else:
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def set_up_toolbar_order(self):
        self.addWidget(self.control.addSaveAnnotationButton())

        self.addSeparator()

        self.addWidget(self.control.addLengthPointsButton())
        self.addWidget(self.control.addDisablePointPickingButton())

        self.addSeparator()

        self.addWidget(self.control.addUndoButton())
        self.addWidget(self.control.addDeleteAllButton())

        self.addSeparator()
        self.addWidget(self.control.addHeightSpinbox())
        self.addSeparator()
        self.addWidget(self.control.addAngleSpinbox())

        self.addSeparator(expand=True)

        self.addWidget(self.control.addTimerButton())

    def addSeparator(self, expand=False):
        if expand:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.addWidget(spacer)
        else:
            spacer = QWidget()
            spacer.setFixedWidth(20)
            self.addWidget(spacer)
