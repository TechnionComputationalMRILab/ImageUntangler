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
            self.cached_pixel_data_dict = {k: None for k, _ in self.sequence_dict.items()}
        else:
            # create and populate the seqfile
            logger.info("Sequence Directory Not Found! Creating...")
            self.sequence_dict = SequenceFile.create_sequence_file(self._list_files_in_directory())
            self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}

    def _list_files_in_directory(self):
        """ generates a list of all the files in the directory """
        f = []
        for (_, _, filenames) in os.walk(self.folder):
            f.extend(filenames)
            break
        return [os.path.join(self.folder, i) for i in f]

    def _generate_pixel_data(self, sequence):
        _list_of_files = self.sequence_dict[sequence]

        _tuple_list = list(zip(#_list_of_files,
                               [float(SequenceFile.get_info('SliceLocation', f)) for f in _list_of_files],
                               [self._get_pixel_array(f) for f in _list_of_files]))
        _tuple_list.sort(key=lambda x: x[0])
        return _tuple_list

    @staticmethod
    def _get_pixel_array(filename):
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        return ds.pixel_array  # can't get this using the getinfo function

    def __getitem__(self, item):
        if item in self.cached_pixel_data_dict.items():
            return self.cached_pixel_data_dict[item]
        else:
            self.cached_pixel_data_dict[item] = self._generate_pixel_data(item)
            return self.cached_pixel_data_dict[item]

    def get_sequence_list(self):
        return list(self.cached_pixel_data_dict.keys())
