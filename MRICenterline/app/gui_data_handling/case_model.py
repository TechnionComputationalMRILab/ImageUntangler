from MRICenterline.app.points.status import PickerStatus, PointStatus, TimerStatus
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

    def __init__(self, path, initial_sequence=None):
        self.path = path
        self.image = GraphicalImager(path)

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

    #########
    # callbacks
    #########

    def change_sequence(self, s):
        logging.info(f"Changing sequence to {self.sequence_list[s]}")
        self.active_sequence_index = s

    def get_case_name(self):
        return self.image.case_name

    #########
    # toolbar
    #########
    def save(self):
        self.sequence_manager.save()

    def set_picker_status(self, status: PickerStatus):
        logging.debug(f"Setting picker status to {status}")
        self.picker_status = status

    def calculate(self, status: PointStatus):
        self.sequence_manager.calculate(status)

    def intermediate_points(self, show: bool):
        self.sequence_manager.intermediate_points(show)

    def timer_status(self, status):
        logging.info(f"Timer set to {status}")
        self.timer.command(status)

    def undo(self, undo_all: bool = False):
        self.sequence_manager.undo(undo_all)

    #########
    # points
    #########

    def pick(self, pick_coords: tuple):
        self.sequence_manager.pick(pick_coords)

    def get_points(self):
        self.sequence_manager.get_points()

    def import_from_v3(self):
        pass

    def load_points(self, length_id, mpr_id):
        self.sequence_manager.load_points(length_id, mpr_id)
