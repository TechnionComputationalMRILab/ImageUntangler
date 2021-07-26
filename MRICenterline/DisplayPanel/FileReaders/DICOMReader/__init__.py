import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
import os
# from icecream import ic

from . import SequenceFile, NumpyToVTK, Header
from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class DICOMReader:
    def __init__(self, folder: str, run_clean=False):
        self.folder = folder
        self.run_clean = run_clean  # if set to true, deletes and re-builds the sequence directory

        self.sequence_dict = dict()
        self.cached_pixel_data_dict = dict()

        self.valid_files = self._get_valid_files()
        self._valid_files_len = len(self.valid_files)

        if self._valid_files_len:
            self._load_sequence_dict()
        else:
            logging.info(f"No DICOM files found in {self.folder}")

    @classmethod
    def test_folder(cls, folder: str):
        _dicom = cls(folder)
        if len(_dicom):
            return _dicom
        else:
            return None

    def _load_sequence_dict(self):
        _seqfile = SequenceFile.check_if_dicom_seqfile_exists(self.folder)
        if _seqfile:
            #             # if seqfile exists, save the seqfile as the dict for the files
            # seqfile is just name of file (not absolute path!) + sequence
            logging.info(f"Sequence Directory Found: {_seqfile}!")
            if self.run_clean:
                os.remove(os.path.join(self.folder, _seqfile))
                self._load_sequence_dict()
            else:
                self.sequence_dict = SequenceFile.load_seqfile(self.folder, _seqfile)
                self.cached_pixel_data_dict = {k: None for k, _ in self.sequence_dict.items()}
        else:
            # create and populate the seqfile
            logging.info("Sequence Directory Not Found! Creating...")
            self.sequence_dict = SequenceFile.create_sequence_file(self.valid_files)
            self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}

    def _list_files_in_directory(self):
        """ generates a list of all the files in the directory """
        f = []
        for (_, _, filenames) in os.walk(self.folder):
            f.extend(filenames)
            break
        return [os.path.join(self.folder, i) for i in f]

    def _get_valid_files(self):
        _files = self._list_files_in_directory()
        _valid_dicom = []
        for f in _files:
            try:
                with open(f, 'rb') as infile:
                    pydicom.dcmread(infile)
            except InvalidDicomError:
                pass
            else:
                _valid_dicom.append(f)
        return _valid_dicom

    def __len__(self):
        """ returns the number of dicom files in the directory """
        return self._valid_files_len

    def _generate_pixel_data(self, sequence):
        _list_of_files = self.sequence_dict[sequence]

        _tuple_list = list(zip(_list_of_files,
                               [float(SequenceFile.get_info('SliceLocation', f)) for f in _list_of_files],
                               [self._get_pixel_array(f) for f in _list_of_files]))
        _tuple_list.sort(key=lambda x: x[1])
        return _tuple_list

    @staticmethod
    def _get_pixel_array(filename):
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        return ds.pixel_array  # can't get this using the getinfo function

    def get_sequence_list(self):
        return list(self.cached_pixel_data_dict.keys())

    def __getitem__(self, item):
        if item in self.cached_pixel_data_dict.items():
            return self.cached_pixel_data_dict[item]
        else:
            self.cached_pixel_data_dict[item] = self._generate_pixel_data(item)
            return self.cached_pixel_data_dict[item]

    def convert_to_vtk(self, seq):
        _prop = NumpyToVTK.get_image_properties([pix[0] for pix in self[seq]])
        _arr = np.array([pix[2] for pix in self[seq]])
        return NumpyToVTK.numpy_array_as_vtk_image_data(_arr,
                                                        origin=_prop['origin'],
                                                        spacing=_prop['spacing'],
                                                        ncomp=_prop['ncomp'],
                                                        direction=_prop['direction'],
                                                        size=_prop['size'])

    def get_header(self, seq):
        return Header.get_header_dict([pix[0] for pix in self[seq]])

    def get_window_and_level(self, seq):
        _arr = np.array([pix[2] for pix in self[seq]])
        _window_percentile = int(CFG.get_config_data('display', 'window-percentile'))
        return int(np.percentile(_arr, _window_percentile)), int(np.percentile(_arr, _window_percentile) / 2)
