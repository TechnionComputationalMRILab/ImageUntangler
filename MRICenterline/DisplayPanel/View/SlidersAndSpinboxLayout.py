from PyQt5.QtWidgets import QLabel, QGridLayout
from MRICenterline.utils import program_constants as CONST


class SlidersAndSpinboxLayout(QGridLayout):
    def __init__(self, window_widgets, level_widgets, index_widgets):
        super().__init__()
        self.list_of_widgets = [("Window", window_widgets), ("Level", level_widgets), ("Slice Index", index_widgets)]

        for row, label in enumerate(CONST.ORDER_OF_CONTROLS):
            self.addWidget(QLabel(label), row, 0)

            for widget in self.list_of_widgets:
                if widget[0] == label:
                    self.addWidget(widget[1]['Slider'], row, 1)
                    self.addWidget(widget[1]['Spinbox'], row, 2)
