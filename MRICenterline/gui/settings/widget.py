from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QStackedWidget, QFileDialog, \
    QLineEdit, QLabel, QGridLayout, QColorDialog, QPushButton, QVBoxLayout, QSizePolicy, \
    QCheckBox, QSpinBox, QComboBox

from MRICenterline import CFG


class PreferencesWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.categories = QListWidget()
        self.categories.insertItem(0, "Folders")
        self.categories.insertItem(1, 'Display')
        self.categories.insertItem(2, "Length style")
        self.categories.insertItem(3, "Centerline style")
        self.categories.insertItem(4, "Dev tools")
        self.categories.currentRowChanged.connect(self.current_category_changed)
        self.categories.setMaximumWidth(200)

        self.main_layout = QHBoxLayout()

        self.preferences = QStackedWidget(self)
        self.preferences.addWidget(self.folders())
        self.preferences.addWidget(self.display())
        self.preferences.addWidget(self.length_display_style())
        self.preferences.addWidget(self.centerline_style())
        self.preferences.setCurrentIndex(0)

        self.main_layout.addWidget(self.categories, stretch=1)
        self.main_layout.addWidget(self.preferences, stretch=3)
        self.setLayout(self.main_layout)

    def current_category_changed(self, i):
        self.preferences.setCurrentIndex(i)

    def folders(self):
        self.default_folder = CFG.get_config_data('folders', 'data-folder')

        def open_dialog():
            _file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

            if _file:
                self.default_folder = _file
                _line_edit.setText(_file)

        _folders_browse_button = QPushButton("Browse...")
        _folders_browse_button.clicked.connect(open_dialog)

        _line_edit = QLineEdit(self.default_folder)

        _folders_widget = QWidget()
        _folders_layout = QVBoxLayout()
        _folders_widget.setLayout(_folders_layout)

        _folders_layout.addWidget(QLabel("Add MRI Images default folder"))
        _folders_layout.addWidget(_line_edit)
        _folders_layout.addWidget(_folders_browse_button)

        SPACER = QWidget()
        SPACER.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        _folders_layout.addWidget(SPACER)

        return _folders_widget

    def display(self):
        # [display]
        # start-maximized = on
        self.start_maximized = CFG.get_boolean('display', 'start-maximized')

        # text-color = 0, 34, 158
        self.panel_text_color = [255*i for i in CFG.get_color('display', 'text-color')]

        # horizontal-number-of-panels = 1
        self.hpanel_number = CFG.get_config_data('display', 'horizontal-number-of-panels')
        # vertical-number-of-panels = 1
        # display-width = 1920
        # display-height = 1080
        # window-percentile = 90
        # dark-mode = False

        def change_color():
            _color_dialog = QColorDialog.getColor()
            self.panel_text_color = _color_dialog.getRgb()[:3]

            _panel_text_color_button.setStyleSheet(
                f'background-color: rgb({self.panel_text_color[0]}, {self.panel_text_color[1]}, {self.panel_text_color[2]}) ')

        def hpanel_spinbox_changed():
            self.hpanel_number = _hpanel_spinbox.value()

        _set_maximized_checkbox = QCheckBox()
        _set_maximized_checkbox.setChecked(self.start_maximized)
        _set_maximized_checkbox.setEnabled(False)

        _panel_text_color_button = QPushButton()
        _panel_text_color_button.setStyleSheet(
            f'background-color: rgb({self.panel_text_color[0]}, {self.panel_text_color[1]}, {self.panel_text_color[2]}) ')
        _panel_text_color_button.clicked.connect(change_color)

        _hpanel_spinbox = QSpinBox()
        _hpanel_spinbox.setRange(1, 4)
        _hpanel_spinbox.valueChanged.connect(hpanel_spinbox_changed)
        _hpanel_spinbox.setEnabled(False)

        _display_widget = QWidget()
        _display_layout = QGridLayout()

        _display_widget.setLayout(_display_layout)
        _display_layout.addWidget(QLabel("Start maximized"), 0, 0)
        _display_layout.addWidget(_set_maximized_checkbox, 0, 1)
        _display_layout.addWidget(QLabel("Panel Text Color"), 1, 0)
        _display_layout.addWidget(_panel_text_color_button, 1, 1)
        _display_layout.addWidget(QLabel("Horizontal Panels"), 2, 0)
        _display_layout.addWidget(_hpanel_spinbox, 2, 1)

        return _display_widget

    def length_display_style(self):
        self.length_color = [255*i for i in CFG.get_color('length-display-style', 'color')]
        self.length_marker_size = int(CFG.get_config_data('length-display-style', 'marker-size'))

        def change_color():
            _color_dialog = QColorDialog.getColor()
            self.length_color = _color_dialog.getRgb()[:3]

            _length_color_button.setStyleSheet(
                f'background-color: rgb({self.length_color[0]}, {self.length_color[1]}, {self.length_color[2]}) ')

        _length_color_button = QPushButton()
        _length_color_button.setStyleSheet(
            f'background-color: rgb({self.length_color[0]}, {self.length_color[1]}, {self.length_color[2]}) ')
        _length_color_button.clicked.connect(change_color)

        def change_marker_size():
            self.length_marker_size = _marker_size_spinbox.value()

        _marker_size_spinbox = QSpinBox()
        _marker_size_spinbox.setRange(1, 5)
        _marker_size_spinbox.setValue(self.length_marker_size)
        _marker_size_spinbox.valueChanged.connect(change_marker_size)

        _marker_type_combox = QComboBox()
        _marker_type_combox.addItems(['Circle', "Square"])
        _marker_type_combox.setEnabled(False)

        _line_style_combox = QComboBox()
        _line_style_combox.setEnabled(False)

        _line_thickness = QSpinBox()
        _line_thickness.setEnabled(False)

        _line_measurement_style = QCheckBox()
        _line_measurement_style.setEnabled(False)

        # layout
        _length_widget = QWidget()
        _length_layout = QGridLayout()
        _length_layout.setColumnStretch(0, 2)
        _length_layout.setColumnStretch(1, 1)
        _length_widget.setLayout(_length_layout)

        _length_layout.addWidget(QLabel("Color"), 0, 0)
        _length_layout.addWidget(_length_color_button, 0, 1)
        _length_layout.addWidget(QLabel("Marker size"), 1, 0)
        _length_layout.addWidget(_marker_size_spinbox, 1, 1)
        _length_layout.addWidget(QLabel("Marker type"), 2, 0)
        _length_layout.addWidget(_marker_type_combox, 2, 1)
        _length_layout.addWidget(QLabel("Line thickness"), 3, 0)
        _length_layout.addWidget(_line_thickness, 3, 1)
        _length_layout.addWidget(QLabel("Line style"), 4, 0)
        _length_layout.addWidget(_line_style_combox, 4, 1)
        _length_layout.addWidget(QLabel("Measurement style"), 5, 0)
        _length_layout.addWidget(_line_measurement_style, 5, 1)

        return _length_widget

    def centerline_style(self):
        self.centerline_color = [255*i for i in CFG.get_color('mpr-display-style', 'color')]
        self.centerline_marker_size = int(CFG.get_config_data('mpr-display-style', 'marker-size'))

        def change_color():
            _color_dialog = QColorDialog.getColor()
            self.centerline_color = _color_dialog.getRgb()[:3]

            _mpr_color_button.setStyleSheet(
                f'background-color: rgb({self.centerline_color[0]}, {self.centerline_color[1]}, {self.centerline_color[2]}) ')

        _mpr_color_button = QPushButton()
        _mpr_color_button.setStyleSheet(
            f'background-color: rgb({self.centerline_color[0]}, {self.centerline_color[1]}, {self.centerline_color[2]}) ')
        _mpr_color_button.clicked.connect(change_color)

        def change_marker_size():
            self.centerline_marker_size = _marker_size_spinbox.value()

        _marker_size_spinbox = QSpinBox()
        _marker_size_spinbox.setRange(1, 5)
        _marker_size_spinbox.setValue(self.centerline_marker_size)
        _marker_size_spinbox.valueChanged.connect(change_marker_size)

        _marker_type_combox = QComboBox()
        _marker_type_combox.addItems(['Circle', "Square"])
        _marker_type_combox.setEnabled(False)

        _line_style_combox = QComboBox()
        _line_style_combox.setEnabled(False)

        _line_thickness = QSpinBox()
        _line_thickness.setEnabled(False)

        _line_measurement_style = QCheckBox()
        _line_measurement_style.setEnabled(False)

        # layout
        _mpr_widget = QWidget()
        _mpr_layout = QGridLayout()
        _mpr_layout.setColumnStretch(0, 2)
        _mpr_layout.setColumnStretch(1, 1)
        _mpr_widget.setLayout(_mpr_layout)

        _mpr_layout.addWidget(QLabel("Color"), 0, 0)
        _mpr_layout.addWidget(_mpr_color_button, 0, 1)
        _mpr_layout.addWidget(QLabel("Marker size"), 1, 0)
        _mpr_layout.addWidget(_marker_size_spinbox, 1, 1)
        _mpr_layout.addWidget(QLabel("Marker type"), 2, 0)
        _mpr_layout.addWidget(_marker_type_combox, 2, 1)
        _mpr_layout.addWidget(QLabel("Line thickness"), 3, 0)
        _mpr_layout.addWidget(_line_thickness, 3, 1)
        _mpr_layout.addWidget(QLabel("Line style"), 4, 0)
        _mpr_layout.addWidget(_line_style_combox, 4, 1)
        _mpr_layout.addWidget(QLabel("Measurement style"), 5, 0)
        _mpr_layout.addWidget(_line_measurement_style, 5, 1)

        return _mpr_widget
