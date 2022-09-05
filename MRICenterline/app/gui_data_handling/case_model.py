from pathlib import Path
from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.points.timer import Timer
from MRICenterline.app.gui_data_handling.gui_imager import GraphicalImager
from MRICenterline.app.gui_data_handling.sequence_model import SequenceModel

import logging
logging.getLogger(__name__)


class CaseModel:
    timer = Timer()
    picker_status = PickerStatus.NOT_PICKING
    sequence_viewer = None
    centerline_model = None

    def __init__(self, path, initial_sequence=None, file_dialog_open=False):
        self.path = path

        if file_dialog_open:
            # if opening through the file dialog box
            self.image = GraphicalImager(path, root_folder=Path(path).parent)
        else:
            self.image = GraphicalImager(path)
        self.window_value, self.level_value = 0, 0

        self.sequence_list = self.image.get_sequences()

        if type(initial_sequence) is str:
            self.active_sequence_index = self.sequence_list.index(initial_sequence)
        else:
            self.active_sequence_index = 0

        self.sequence_manager = SequenceModel(self)

    def set_sequence_viewer(self, sequence_viewer):
        self.sequence_viewer = sequence_viewer

    def set_centerline_model(self, centerline_model):
        self.centerline_model = centerline_model

    # region callbacks
    def change_sequence(self, s):
        logging.info(f"Changing sequence to {self.sequence_list[s]}")
        self.active_sequence_index = s

    def get_case_name(self):
        return self.image.case_name

    def update_window_level(self):
        self.window_value, self.level_value = self.sequence_manager.update_window_level()

        if self.centerline_model:
            self.centerline_model.set_window_level(self.window_value, self.level_value)

    def print_status_to_terminal(self):
        logging.info(f'''
            Image path: {self.path}
            Case name: {self.get_case_name()}
            Picker status: {self.picker_status}
            Window/Level: {self.window_value, self.level_value}
            Centerline: {True if self.centerline_model else False}
            Image details:
                Origin: {self.image.properties.origin}
                Spacing: {self.image.properties.spacing}
                Size: {self.image.properties.size}
        ''')

        self.sequence_manager.print_status_to_terminal()

    def mpr_marker_highlight(self, index: int):
        self.sequence_manager.highlight_point(index, PointStatus.MPR, select_from_mpr_panel=True)

    # endregion

    # region toolbar
    def save(self):
        session_id = self.sequence_manager.save()

        if self.centerline_model:
            self.centerline_model.save()

        return session_id

    def export(self, destination: str, display_options: dict, centerline_options: dict):
        # self.sequence_manager.export(destination, display_options)

        if self.centerline_model:
            self.centerline_model.export(destination, centerline_options)

    def set_picker_status(self, status: PickerStatus):
        logging.debug(f"Setting display panel picker status to {status}")
        self.picker_status = status

        if self.centerline_model and not (status == PickerStatus.PICKING_MPR or status == PickerStatus.MODIFYING_MPR):
            self.centerline_model.set_picker_status(status)

    def calculate(self, status: PointStatus):
        self.sequence_manager.calculate(status)

        if self.centerline_model:
            self.centerline_model.calculate_length()

    def timer_status(self, status):
        import time

        logging.info(f"Timer set to {status} on {int(time.time())}")
        self.timer.command(status)

    def undo(self, undo_all: bool = False):
        self.sequence_manager.undo(undo_all)

    def toggle_mpr_marker_visibility(self, show: bool):
        if self.centerline_model:
            self.centerline_model.toggle_mpr_marker(show)

    # endregion

    # region points
    def intermediate_points(self, show: bool):
        self.sequence_manager.intermediate_points(not show)

    def find_point(self):
        self.picker_status = PickerStatus.FIND_MPR

        if self.centerline_model:
            self.centerline_model.set_picker_status(PickerStatus.FIND_MPR)

    def pick(self, pick_coords: tuple):
        self.sequence_manager.pick(pick_coords)

    def get_points(self):
        self.sequence_manager.get_points()

    def load_points(self, length_id, mpr_id):
        self.sequence_manager.load_points(length_id, mpr_id)

    def point_shift(self, direction: str):
        logging.debug(f"Point shift triggered: {direction}")
        self.sequence_manager.point_shift(direction)
    # endregion
