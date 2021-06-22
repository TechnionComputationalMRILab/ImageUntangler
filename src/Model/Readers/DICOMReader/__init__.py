import pydicom
from typing import List
import numpy as np
import os
import json

from . import SequenceFile

from util import logger
logger = logger.get_logger()


class DICOMReader:
    """
    properties:
        folder
        sequence_dict
    """
    def __init__(self, folder: str):
        self.folder = folder

        self._load_sequence_dict()

    def _load_sequence_dict(self):
        _seqfile = SequenceFile.check_if_dicom_seqfile_exists(self.folder)
        if _seqfile:
            # if seqfile exists, save the seqfile as the dict for the files
            # seqfile is just name of file (not absolute path!) + sequence
            logger.info(f"Sequence Directory Found in {self.folder}!")
            self.sequence_dict = SequenceFile.load_seqfile(self.folder, _seqfile)
            self.cached_seq = 0 # TODO
        else:
            # create and populate the seqfile
            logger.info("Sequence Directory Not Found! Creating...")
            self.sequence_dict = SequenceFile.create_sequence_file(self._list_files_in_directory())

    def _list_files_in_directory(self):
        """ generates a list of all the files in the directory """
        f = []
        for (_, _, filenames) in os.walk(self.folder):
            f.extend(filenames)
            break
        return [os.path.join(self.folder, i) for i in f]

    def __getitem__(self, item):
        pass