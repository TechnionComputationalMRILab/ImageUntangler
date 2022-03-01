import shutil
import tempfile
import sqlite3
import pydicom
import numpy as np
import os
from glob import glob
import SimpleITK as sitk
from pathlib import Path

from . import SequenceFile, NumpyToVTK, Header, GenerateMetadata
from . import InitialDatabaseBuild
from MRICenterline.FileReaders.AbstractReader import AbstractReader
from MRICenterline.Config import CFG

import logging
logging.getLogger(__name__)


class DICOMReader(AbstractReader):
    def __init__(self, case_id, folder, is_new_case):
        super().__init__(case_id, folder, is_new_case)

        if self.is_new_case:
            InitialDatabaseBuild.build(self.folder)
        self.read_from_database()

    def __repr__(self):
        return f"DICOMReader for case with ID [{self.case_id}], with [{len(self)}] sequences."

    def __getitem__(self, item) -> np.ndarray:
        if type(item) is int:
            return self[self.sequence_list[item]]
        elif (type(item) is str) and (item in self.sequence_list):
            return self.generate_simple_itk_image(self.get_file_list(item))
        else:
            raise KeyError("Sequence not found in DICOMReader")

    def read_from_database(self):
        con = sqlite3.connect(CFG.get_db())
        self.sequence_list = [item[0] for item in con.cursor().execute("select name from 'sequences' where case_id=(?)",
                                                                       (self.case_id, )).fetchall()]
        self.sequence_list.remove("INVALID")
        con.close()

    def get_file_list(self, seq):
        con = sqlite3.connect(CFG.get_db())
        if type(seq) is str:
            query = f"""
                    SELECT filename FROM sequences
                    inner join sequence_files
                    on sequences.seq_id = sequence_files.seq_id
                    where sequences.name = '{seq}'
                    and sequence_files.case_id = {self.case_id};
                    """
            sequence_files = [item[0] for item in con.cursor().execute(query).fetchall()]
            con.close()
            return [os.path.join(self.folder, i) for i in sequence_files]
        elif type(seq) is int:
            return self.get_file_list(self.sequence_list[seq])
        else:
            raise KeyError("Sequence not found in database")

    @staticmethod
    def generate_simple_itk_image(file_list):
        # TODO: remove dependency on tempdir , it's a temporary fix to a possible sITK bug
        reader = sitk.ImageSeriesReader()

        with tempfile.TemporaryDirectory() as temp_dir:
            for fi in file_list:
                shutil.copy(src=fi, dst=temp_dir)

            dicom_names = reader.GetGDCMSeriesFileNames(temp_dir)
            reader.SetFileNames(dicom_names)
            image = reader.Execute()

        return image



    # def _load_sequence_dict(self):
    #     _seqfile = SequenceFile.check_if_dicom_seqfile_exists(self.folder)
    #     if _seqfile:
    #         # if seqfile exists, save the seqfile as the dict for the files
    #         # seqfile is just name of file (not absolute path!) + sequence
    #         logging.info(f"Sequence Directory Found: {_seqfile}!")
    #         if self.run_clean:
    #             try:
    #                 os.remove(os.path.join(self.folder, _seqfile))
    #             except:
    #                 pass
    #
    #             self._load_sequence_dict()
    #             self.run_clean = False
    #         else:
    #             self.cached_pixel_data_dict = {k: None for k, _ in self.sequence_dict.items()}
    #     else:
    #         # create and populate the seqfile
    #         logging.info("Sequence Directory Not Found! Creating...")
    #         SequenceFile.create_sequence_file(self.folder, self.sequence_dict)
    #         self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}
    #
    # def check_seqfile_exists(self):
    #     if SequenceFile.check_if_dicom_seqfile_exists(self.folder):
    #         return True
    #     else:
    #         return False
    #
    # def generate_seq_dict(self):
    #     """ to be used with BulkFolderScanner """
    #     self.cached_pixel_data_dict = {k: list() for k, _ in self.sequence_dict.items()}
    #
    # def _list_files_in_directory(self):
    #     """ generates a list of all the files in the directory """
    #     return [Path(file) for file in glob(f'{self.folder}/*.dcm')]
    #
    # def __len__(self):
    #     """ returns the number of dicom files in the directory """
    #     return len(self.sequence_dict)
    #
    # def _generate_pixel_data(self, sequence):
    #     _list_of_files = [os.path.join(self.folder, i) for i in self.sequence_dict[sequence]]
    #
    #     # _tuple_list = list(zip(_list_of_files,
    #     #                        [float(SequenceFile.get_info('SliceLocation', f)) for f in _list_of_files],
    #     #                        [self._get_pixel_array(f) for f in _list_of_files]))
    #     _tuple_list = list(zip(_list_of_files,
    #                            [float(SequenceFile.get_info('SliceLocation', f)) for f in _list_of_files],
    #                            self._get_sitk_image_volume(_list_of_files)))
    #
    #     _tuple_list.sort(key=lambda x: x[1])
    #     return _tuple_list
    #
    # @staticmethod
    # def _get_pixel_array(filename):
    #     with open(filename, 'rb') as f:
    #         ds = pydicom.dcmread(f)
    #     return ds.pixel_array  # can't get this using the getinfo function
    #
    # def _get_sitk_image_volume(self, file_list):
    #     reader = sitk.ImageSeriesReader()
    #     reader.SetFileNames(file_list)
    #     image = reader.Execute()
    #     self.sitk_image = image
    #
    #     # print(image.GetDirection())
    #     # direction = [1.0, 0.0, 0.0,
    #     #              0.0, 0.0, 1.0,
    #     #              0.0, -1.0, 0.0]
    #     #
    #     # image.SetDirection(direction)
    #     pixel_data = sitk.GetArrayFromImage(image)
    #     return pixel_data
    #
    # def get_sequence_list(self):
    #     return list(self.sequence_dict.keys())
    #
    # def __getitem__(self, item):
    #     if item in self.cached_pixel_data_dict.items():
    #         return self.cached_pixel_data_dict[item]
    #     else:
    #         self.cached_pixel_data_dict[item] = self._generate_pixel_data(item)
    #         return self.cached_pixel_data_dict[item]
    #
    # def convert_to_vtk(self, seq):
    #     _prop, _ = NumpyToVTK.get_image_properties([pix[0] for pix in self[seq]])
    #     _arr = np.array([pix[2] for pix in self[seq]])
    #     return NumpyToVTK.numpy_array_as_vtk_image_data(_arr,
    #                                                     origin=_prop['origin'],
    #                                                     spacing=_prop['spacing'],
    #                                                     ncomp=_prop['ncomp'],
    #                                                     direction=_prop['direction'],
    #                                                     size=_prop['size'])
    #
    # def get_numpy(self, seq):
    #     _prop, _ = NumpyToVTK.get_image_properties([pix[0] for pix in self[seq]])
    #     _arr = np.array([pix[2] for pix in self[seq]])
    #     return _arr
    #
    # def get_z_coords_list(self, seq):
    #     return [pix[1] for pix in self[seq]]
    #
    # def get_header(self, seq):
    #     return Header.get_header_dict([pix[0] for pix in self[seq]])
    #
    # def get_window_and_level(self, seq):
    #     _arr = np.array([pix[2] for pix in self[seq]])
    #     _window_percentile = int(CFG.get_config_data('display', 'window-percentile'))
    #     return int(np.percentile(_arr, _window_percentile)), int(np.percentile(_arr, _window_percentile) / 2)
    #
    # def generate_report(self, required_fields):
    #     _dict = {}
    #     for field in required_fields:
    #         try:
    #             _dict[field] = SequenceFile.get_info(field, self.sequence_dict[0])
    #         except KeyError:
    #             _dict[field] = ""
    #
    #     _dict["Sequences"] = list(self.sequence_dict)
    #     return _dict
