import sqlite3

from datetime import datetime, timezone

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MRICenterline.app.gui_data_handling.sequence_viewer import SequenceViewer
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.gui.vtk.interactor_style import SequenceViewerInteractorStyle
from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class SequenceModel:

    def __init__(self, model):
        self.seq_idx = -1
        self.model = model
        self.image = self.model.image

    def change_window(self, window):
        self.model.change_window(window)

    def change_level(self, level):
        self.model.change_level(level)

    def __repr__(self):
        return f"Viewer Manager with index {self.seq_idx}"

    def load_sequence(self, seq_idx: int, interactor: QVTKRenderWindowInteractor,
                      interactor_style: SequenceViewerInteractorStyle):
        logging.debug(f"Loading sequence {seq_idx} / {self.image.get_sequences()[seq_idx]}")
        image_properties: ImageProperties = self.image[seq_idx]

        sequence_viewer = SequenceViewer(viewer_manger=self,
                                         image_properties=image_properties,
                                         interactor=interactor,
                                         interactor_style=interactor_style)
        self.append_to_case_history(seq_idx)
        self.model.set_sequence_viewer(sequence_viewer)

        self.seq_idx = seq_idx
        self.model.change_sequence(self.seq_idx)
        return sequence_viewer

    def append_to_case_history(self, seq_idx):
        # get case and sequence id
        case_id = self.image.get_case_id()
        seq_id = self.image.get_sequences()[seq_idx]
        timestamp = datetime.now(timezone.utc).astimezone().strftime(CONST.TIMESTAMP_FORMAT)

        con = sqlite3.connect(CFG.get_db())
        with con:
            con.execute('insert into case_access_history (case_id, seq_id, timestamp) values (?, ?, ?)',
                        (case_id, seq_id, timestamp))
        con.close()
