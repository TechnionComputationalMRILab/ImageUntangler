from MRICenterline.app.database.save_points import save_points

from MRICenterline.app.points.status import PickerStatus, PointStatus, TimerStatus
from MRICenterline.app.points.timer import Timer
from MRICenterline.app.gui_data_handling.gui_imager import GraphicalImager
from MRICenterline.app.gui_data_handling.sequence_model import SequenceModel
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray

import logging
logging.getLogger(__name__)


class CaseModel:
    timer = Timer()
    picker_status = PickerStatus.NOT_PICKING
    sequence_viewer = None
    mpr_point_array = PointArray(PointStatus.MPR)
    length_point_array = PointArray(PointStatus.LENGTH)

    def __init__(self, path, initial_sequence_index: int = 0):
        self.path = path
        self.image = GraphicalImager(path)

        self.sequence_list = self.image.get_sequences()

        self.active_sequence_index = initial_sequence_index \
            if initial_sequence_index in range(len(self.sequence_list)) else 0

        self.sequence_manager = SequenceModel(self)

    def set_sequence_viewer(self, sequence_viewer):
        self.sequence_viewer = sequence_viewer

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
        logging.info("Saving points")
        save_points(case_name=self.image.case_name,
                    sequence_name=self.sequence_list[self.active_sequence_index],
                    length_points=self.length_point_array,
                    mpr_points=self.mpr_point_array,
                    timer_data=self.timer)

    def set_picker_status(self, status: PickerStatus):
        logging.debug(f"Setting picker status to {status}")
        self.picker_status = status

    def calculate(self, status: PointStatus):
        if status == PointStatus.MPR:
            pass
        elif status == PointStatus.LENGTH:
            pass

    def intermediate_points(self, show: bool):
        if show:
            self.mpr_point_array.show_intermediate_points()
        else:
            self.mpr_point_array.hide_intermediate_points()

        # refresh the renderer
        self.sequence_viewer.render_panel()

    def timer_status(self, status: TimerStatus):
        print(status)

    def undo(self, undo_all: bool = False):
        if undo_all:
            while len(self.length_point_array) > 0:
                self.length_point_array.delete(-1)

            while len(self.mpr_point_array) > 0:
                self.mpr_point_array.delete(-1)

        else:
            logging.info("Undo last point")
            if (self.picker_status == PickerStatus.PICKING_LENGTH) and (len(self.length_point_array) > 0):
                self.length_point_array.delete(-1)
            if (self.picker_status == PickerStatus.PICKING_MPR) and (len(self.mpr_point_array) > 0):
                self.mpr_point_array.delete(-1)

        # refresh the renderer
        self.sequence_viewer.render_panel()

    #########
    # points
    #########

    def pick(self, pick_coords: tuple):
        slice_index = self.sequence_viewer.slice_idx
        point = Point(pick_coords, slice_index, self)
        logging.debug(f"{self.picker_status} | {point}")

        # if self.picker_status == PickerStatus.PICKING_MPR:
            # self.mpr_point_array.add_point(point)
            # self.sequence_viewer.add_point_actor(self.mpr_point_array.get_last_actor())

        if self.picker_status == PickerStatus.PICKING_LENGTH:
            self.length_point_array.add_point(point)
            self.sequence_viewer.add_point_actor(self.length_point_array.get_last_actor())
        logging.debug(f"[{len(self.length_point_array)}] length points, [{len(self.mpr_point_array)}] MPR points")

    def get_points(self):
        if len(self.length_point_array):
            print(self.length_point_array)
        if len(self.mpr_point_array):
            print(self.mpr_point_array)
