from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QComboBox, QSizePolicy, QSpinBox, QGridLayout, QLabel

from MRICenterline.app.config.internal_config import ORDER_OF_CONTROLS

import logging
logging.getLogger(__name__)


class SequenceInteractorWidgets:
    def __init__(self, model, parent_widget=None):
        self.parent = parent_widget
        self.model = model
        sequence_list = self.model.sequence_list

        # initialize sequence combo box
        self.sequence_combo_box = QComboBox(parent=self.parent)
        [self.sequence_combo_box.addItem(name) for name in sequence_list]

        combo_box_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        combo_box_size_policy.setHorizontalStretch(0)
        combo_box_size_policy.setVerticalStretch(0)
        combo_box_size_policy.setHeightForWidth(self.sequence_combo_box.sizePolicy().hasHeightForWidth())

        # initialize sliders
        self.index_slider = QSlider(Qt.Horizontal, parent=self.parent)
        self.window_slider = QSlider(Qt.Horizontal, parent=self.parent)
        self.level_slider = QSlider(Qt.Horizontal, parent=self.parent)

        # initialize spin boxes
        self.index_spinbox = QSpinBox(parent=self.parent)
        self.window_spinbox = QSpinBox(parent=self.parent)
        self.level_spinbox = QSpinBox(parent=self.parent)

        self.index_widgets = {"Slider": self.index_slider,
                              "Spinbox": self.index_spinbox
                              }
        self.window_widgets = {"Slider": self.window_slider,
                               "Spinbox": self.window_spinbox
                              }
        self.level_widgets = {"Slider": self.level_slider,
                              "Spinbox": self.level_spinbox
                              }

        self.add_actions()

    def setParent(self, parent):
        self.parent = parent

    def set_index(self, index):
        self.index_slider.setValue(index)
        self.index_spinbox.setValue(index)

    def set_window(self, window):
        self.window_slider.setValue(window)
        self.window_spinbox.setValue(window)

    def set_level(self, level):
        self.level_spinbox.setValue(level)
        self.level_slider.setValue(level)

    def freeze_sequence_list(self, text):
        self.sequence_combo_box.setEnabled(False)
        self.sequence_combo_box.setItemText(0, text)

    def add_actions(self):
        self.sequence_combo_box.currentIndexChanged.connect(self.model.change_sequence)

        self.index_slider.sliderMoved.connect(self.model.change_index)
        self.window_slider.sliderMoved.connect(self.model.change_window)
        self.level_slider.sliderMoved.connect(self.model.change_level)

        self.index_spinbox.valueChanged.connect(self.model.change_index)
        self.window_spinbox.valueChanged.connect(self.model.change_window)
        self.level_spinbox.valueChanged.connect(self.model.change_level)

    def initialize_values(self, slice_index: int, max_slice: int, window_value: int, level_value: int) -> None:
        self.index_slider.setMinimum(1)
        self.index_slider.setMaximum(max_slice)
        self.index_slider.setValue(slice_index)

        self.index_spinbox.setMinimum(1)
        self.index_spinbox.setMaximum(max_slice)
        self.index_spinbox.setValue(slice_index)

        self.window_slider.setMaximum(int(2.5 * window_value))
        self.window_slider.setMinimum(max(1, window_value - 800))
        self.window_slider.setValue(window_value)

        self.window_spinbox.setMaximum(int(2.5 * window_value))
        self.window_spinbox.setMinimum(max(1, window_value - 800))
        self.window_spinbox.setValue(window_value)

        self.level_slider.setMinimum(max(level_value - 400, 1))
        self.level_slider.setMaximum(int(level_value * 2.5))
        self.level_slider.setValue(level_value)

        self.level_spinbox.setMinimum(max(level_value - 400, 1))
        self.level_spinbox.setMaximum(int(level_value * 2.5))
        self.level_spinbox.setValue(level_value)

    def reset_sliders(self, window_value: int, level_value: int):
        self.window_slider.setMaximum(int(2.5 * window_value))
        self.window_slider.setMinimum(max(window_value - 900, 1))
        self.window_slider.setValue(window_value)

        self.level_slider.setMinimum(max(level_value - 500, 1))
        self.level_slider.setMaximum(int(level_value * 2.5))
        self.level_slider.setValue(level_value)

    def build_group_box(self):
        group_box = QGridLayout()

        list_of_widgets = [("Window", self.window_widgets),
                                ("Level", self.level_widgets),
                                ("Slice Index", self.index_widgets)]

        for row, label in enumerate(ORDER_OF_CONTROLS):
            group_box.addWidget(QLabel(label), row, 0)

            for widget in list_of_widgets:
                if widget[0] == label:
                    group_box.addWidget(widget[1]['Slider'], row, 1)
                    group_box.addWidget(widget[1]['Spinbox'], row, 2)

        return group_box
