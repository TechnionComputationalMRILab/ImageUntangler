import sqlite3

from datetime import datetime, timezone

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.DisplayPanel.View.GenericSequenceViewer import GenericSequenceViewer

from MRICenterline.utils import program_constants as CONST, message as MSG
from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


class GenericViewerManager:
    def __init__(self, model, imager: Imager):
        self.imager = imager
        self.seq_idx = -1 # index of image that is properly encoded
        self.manager = model

    def changeWindow(self, window):
        self.manager.changeWindow(window)

    def changeLevel(self, level):
        self.manager.changeLevel(level)

    def updateSliderIndex(self, index):
        self.manager.updateSliderIndex(index)

    # def showValidImage(self, sequenceIndex: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
    #     logging.debug(f"showValidImage function run. sequenceIndex: {sequenceIndex}")
    #     if self.goodIndex == -1: # first image is being loaded
    #         if sequenceIndex == len(self.MRIimages)-1:
    #             logging.error("Bad files?")
    #             MSG.msg_box_warning("Bad files!")
    #         else:
    #             return self.loadSequence(sequenceIndex+1, VTKinteractor, interactorStyle)
    #     else:
    #         logging.error("gzip files?")
    #         MSG.msg_box_warning("GZip files, but you shouldnt be seeing this error")
    #         return self.loadSequence(self.goodIndex, VTKinteractor, interactorStyle)

    def loadSequence(self, seq_idx: int, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle):
        try:
            logging.debug(f"Loading sequence {seq_idx} / {self.imager.get_sequences()[seq_idx]}")

            sequenceViewer = GenericSequenceViewer(self, VTKinteractor, interactorStyle, self.imager[seq_idx])
        except Exception as err:
            logging.critical(f"Error in loading sequence. Error is {err}")
        else:
            self.append_to_case_history(seq_idx)
            _ = sequenceViewer.sliceIdx

            self.seq_idx = seq_idx
            self.manager.setListWidgetIndex(self.seq_idx)
            return sequenceViewer

    def load_single_sequence(self, VTKinteractor: QVTKRenderWindowInteractor, interactorStyle,
                             single_image, sequence_index):
        logging.debug(f"Loading single sequence")

        self.seq_idx = sequence_index
        self.append_to_case_history(sequence_index)
        return GenericSequenceViewer(self, VTKinteractor, interactorStyle, single_image)

    def append_to_case_history(self, seq_idx):
        # get case and sequence id
        seq_id = self.imager.get_sequences()[seq_idx]
        case_id = self.imager.get_case_id()
        timestamp = datetime.now(timezone.utc).astimezone().strftime(CONST.TIMESTAMP_FORMAT)

        ic(datetime.now(timezone.utc).astimezone())

        con = sqlite3.connect(CFG.get_db())
        with con:
            con.execute('insert into case_access_history (case_id, seq_id, timestamp) values (?, ?, ?)',
                                                         (case_id, seq_id, timestamp))
        con.close()
