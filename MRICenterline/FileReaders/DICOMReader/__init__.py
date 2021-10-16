import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
import os
from glob import glob
from pathlib import Path

from . import SequenceFile, NumpyToVTK, Header, GenerateMetadata
from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class DICOMReader:
    def __init__(self, folder: str, run_clean=False):
        self.folder = folder
        self.run_clean = run_clean  # if set to true, deletes and re-builds the sequence directory

        self._check_data_folder()

        self._files_list = [file.replace('\\', '/') for file in glob(f'{self.folder}/*.dcm')]
        self.sequence_dict = SequenceFile.generate_seqlist_dict(self._files_list)
        self.cached_pixel_data_dict = dict()

        if self.sequence_dict:
            self._load_sequence_dict()
            # self._load_metadata_dict()
        else:
            logging.info(f"No DICOM files found in {self.folder}")

    def _check_data_folder(self):
        if self.folder.endswith('data'):
            self.folder = self.folder.replace('data', '')

        # create the data folder if it doesnt exist
        if not os.path.exists(os.path.join(self.folder, 'data')):
            logging.info("Creating data directory")
            Path(os.path.join(self.folder, 'data')).mkdir()
        else:
            logging.info("Loading from data directory")

        #   check for any annotation files
        _annotation_files = glob(os.path.join(self.folder, 'data') + "/*.annotation.json")
        if len(_annotation_files):
            logging.info(f"Found {len(_annotation_files)} annotation files")

    def _load_metadata_dict(self):
        if not os.path.exists(os.path.join(self.folder, 'data', 'metadata.json')):
            logging.debug("Creating metadata file")
            _metadata_dict = GenerateMetadata.get(self.sequence_dict)
            print(_metadata_dict)
            GenerateMetadata.save(_metadata_dict, self.folder)
            logging.info(f"Metadata file saved in {os.path.join(self.folder, 'data', 'metadata.json')}")
        else:
            logging.debug("Loading metadata file")

    @classmethod
    def test_folder(cls, folder: str, run_clean=False):
        _dicom = cls(folder, run_clean)
        if len(_dicom):
            return _dicom
        else:
            return None

    def _load_sequence_dict(self):
        _seqfile = SequenceFile.check_if_dicom_seqfile_exists(self.folder)
        if _seqfile:
            # if seqfile exists, save the seqfile as the dict for the files
            # seqfile is just name of file (not absolute path!) + sequence
            logging.info(f"Sequence Directory Found: {_seqfile}!")
            if self.run_clean:
                os.remove(os.path.join(self.folder, _seqfile))
                self._load_sequence_dict()
                self.run_clean = False
            else:
                self.cached_pixel_data_dict = {k: None for k, _ in self.sequence_dict.items()}
        else:
            # create and populate the seqfile
            logging.info("Sequence Directory Not Found! Creating...")
            SequenceFile.create_sequence_file(self.folder, self.sequence_dict)
            self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}

    def check_seqfile_exists(self):
        if SequenceFile.check_if_dicom_seqfile_exists(self.folder):
            return True
        else:
            return False

    def generate_seq_dict(self):
        """ to be used with BulkFolderScanner """
        self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}

    def _list_files_in_directory(self):
        """ generates a list of all the files in the directory """
        return [file.replace('\\', '/') for file in glob(f'{self.folder}/*.dcm')]

    # def _get_valid_files(self):
    #     _files = self._list_files_in_directory()
    #     _valid_dicom = []
    #     for f in _files:
    #         try:
    #             with open(f, 'rb') as infile:
    #                 pydicom.dcmread(infile)
    #         except InvalidDicomError:
    #             pass
    #         else:
    #             _valid_dicom.append(f)
    #     return _valid_dicom

    def __len__(self):
        """ returns the number of dicom files in the directory """
        return len(self.sequence_dict)

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
        return list(self.sequence_dict.keys())

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

    def get_z_coords_list(self, seq):
        return [pix[1] for pix in self[seq]]

    def get_header(self, seq):
        return Header.get_header_dict([pix[0] for pix in self[seq]])

    def get_window_and_level(self, seq):
        _arr = np.array([pix[2] for pix in self[seq]])
        _window_percentile = int(CFG.get_config_data('display', 'window-percentile'))
        return int(np.percentile(_arr, _window_percentile)), int(np.percentile(_arr, _window_percentile) / 2)

    def generate_report(self, required_fields):
        _dict = {}
        for field in required_fields:
            try:
                _dict[field] = SequenceFile.get_info(field, self.sequence_dict[0])
            except KeyError:
                _dict[field] = ""

        _dict["Sequences"] = list(self.sequence_dict)
        return _dict
