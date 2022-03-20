import sqlite3

from datetime import datetime, timezone

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MRICenterline.app.database.save_points import save_points
from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.gui_data_handling.sequence_viewer import SequenceViewer
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.gui.vtk.interactor_style import SequenceViewerInteractorStyle

from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray


from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class SequenceModel:
    def __init__(self, model):
        self.seq_idx = -1
        self.model = model
        self.image = self.model.image

        self.current_sequence_viewer = None
        self.current_image_properties = None

        self.mpr_point_array = PointArray(PointStatus.MPR)
        self.length_point_array = PointArray(PointStatus.LENGTH)

    def change_window(self, window):
        pass
        # self.model.change_window(window)

    def change_level(self, level):
        pass
        # self.model.change_level(level)

    def __repr__(self):
        return f"Viewer Manager with index {self.seq_idx}"

    def load_sequence(self, seq_idx: int, interactor: QVTKRenderWindowInteractor,
                      interactor_style: SequenceViewerInteractorStyle):
        logging.debug(f"Loading sequence {seq_idx} / {self.image.get_sequences()[seq_idx]}")
        self.seq_idx = seq_idx
        image_properties: ImageProperties = self.image[seq_idx]
        self.current_image_properties = image_properties

        sequence_viewer = SequenceViewer(viewer_manger=self,
                                         image_properties=image_properties,
                                         interactor=interactor,
                                         interactor_style=interactor_style)
        self.append_to_case_history()
        self.model.set_sequence_viewer(sequence_viewer)
        self.current_sequence_viewer = sequence_viewer
        self.model.change_sequence(self.seq_idx)
        return sequence_viewer

    def append_to_case_history(self):
        # get case and sequence id
        case_id = self.image.get_case_id()
        seq_id = self.image.get_sequences()[self.seq_idx]
        timestamp = datetime.now(timezone.utc).astimezone().strftime(CONST.TIMESTAMP_FORMAT)

        con = sqlite3.connect(CFG.get_db())
        with con:
            con.execute('insert into case_access_history (case_id, seq_id, timestamp) values (?, ?, ?)',
                        (case_id, seq_id, timestamp))
        con.close()

    def save(self):
        logging.info("Saving points")
        save_points(case_name=self.image.case_name,
                    sequence_name=self.image.get_sequences()[self.seq_idx],
                    length_points=self.length_point_array,
                    mpr_points=self.mpr_point_array,
                    timer_data=self.model.timer)

    def calculate(self, status: PointStatus):
        from MRICenterline.app.centerline.calculate import PointsToPlaneVectors

        if status == PointStatus.MPR: #TODO
            self.centerline_data = 0.0
            # ppv = PointsToPlaneVectors(self.mpr_point_array.get_as_np_array(),
            #                      self.current_image_properties)
            # print(ppv.MPR_M)

        elif status == PointStatus.LENGTH:
            print(self.length_point_array.lengths)
            print(self.length_point_array.total_length)

    def intermediate_points(self, show: bool):
        if show:
            self.mpr_point_array.show_intermediate_points()
        else:
            self.mpr_point_array.hide_intermediate_points()

        # refresh the renderer
        self.current_sequence_viewer.render_panel()

    def undo(self, undo_all: bool = False):
        if undo_all:
            while len(self.length_point_array) > 0:
                self.length_point_array.delete(-1)

            while len(self.mpr_point_array) > 0:
                self.mpr_point_array.delete(-1)

        else:
            logging.info("Undo last point")
            if (self.model.picker_status == PickerStatus.PICKING_LENGTH) and (len(self.length_point_array) > 0):
                self.length_point_array.delete(-1)
            if (self.model.picker_status == PickerStatus.PICKING_MPR) and (len(self.mpr_point_array) > 0):
                self.mpr_point_array.delete(-1)

        # refresh the renderer
        self.current_sequence_viewer.render_panel()

    def pick(self, pick_coords: tuple):


        slice_index = self.current_sequence_viewer.slice_idx
        point = Point(pick_coords, slice_index, self.current_image_properties)
        logging.debug(f"{self.model.picker_status} | {point}")

        if self.model.picker_status == PickerStatus.PICKING_MPR:
            self.mpr_point_array.add_point(point)
            self.current_sequence_viewer.add_actor(self.mpr_point_array.get_last_actor())

        if self.model.picker_status == PickerStatus.PICKING_LENGTH:
            self.length_point_array.add_point(point)
            self.current_sequence_viewer.add_actor(self.length_point_array.get_last_actor())

        logging.debug(f"[{len(self.length_point_array)}] length points, [{len(self.mpr_point_array)}] MPR points")

    def get_points(self):
        from MRICenterline.gui.points.dialog_box import PointDialogBox
        pdb = PointDialogBox(self)
        pdb.exec()

    def load_points(self, length_id, mpr_id):
        print(f"loading {length_id}")
        print(f"loading {mpr_id}")
