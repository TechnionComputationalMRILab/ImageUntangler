import shutil
import tempfile
import sqlite3
import os
import SimpleITK as sitk

from MRICenterline.app.database import name_id
from MRICenterline.app.file_reader.dicom import InitialDatabaseBuild, constants, DICOMImageOrientation
from MRICenterline.app.file_reader.AbstractReader import AbstractReader, ImageOrientation

from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


class DICOMReader(AbstractReader):
    def __init__(self, case_id, case_name, folder, is_new_case):
        super().__init__(case_id, case_name, folder, is_new_case)

        if self.is_new_case:
            InitialDatabaseBuild.build(self.folder, case_name)
        self.read_from_database()

    def __repr__(self):
        return f"DICOMReader for case with ID [{self.case_id}], with [{len(self)}] sequences."

    def __getitem__(self, item):
        if type(item) is int:
            return self[self.sequence_list[item]]
        elif (type(item) is str) and (item in self.sequence_list):
            try:
                return self.generate(self.get_file_list(item))
            except FileNotFoundError:
                MSG.msg_box_warning("File not found",
                                    should_crash=True,
                                    details="Possible config/database mismatch. Please check config.ini",
                                    info="Program will now close")
                logging.error("File not found. Probably an error with the raw-data folder set in config.ini")
        else:
            raise KeyError("Sequence not found in DICOMReader")

    def find_index_from_seq_id(self, seq_id):
        seq_name = name_id.get_sequence_name(seq_id, self.case_id)
        return self.sequence_list.index(seq_name)

    def read_from_database(self):
        con = sqlite3.connect(CFG.get_db())
        self.sequence_list = [item[0]
                              for item in con.cursor().execute("select name from 'sequences' where case_id=(?)",
                                                               (self.case_id, )).fetchall()]

        if 'INVALID' in self.sequence_list:
            self.sequence_list.remove("INVALID")
        else:
            pass

        con.close()

    def get_file_list(self, seq, use_v3=False):
        if CFG.get_testing_status("use-slice-location") or use_v3:
            con = sqlite3.connect(CFG.get_db())

            if type(seq) is str:
                query = f"""
                         select distinct filename, slice_location from slice_locations
                         inner join sequence_files
                         on sequence_files.file_id = slice_locations.file_id
                         inner join sequences
                         on sequences.seq_id = sequence_files.seq_id
                         where sequences.name = '{seq}'
                         and sequence_files.case_id = {self.case_id}
                         order by slice_location asc;
                         """
                file_and_slice_list = [(item[0], item[1]) for item in con.cursor().execute(query).fetchall()]
                con.close()
                return [(os.path.join(self.folder, f), loc) for f, loc in file_and_slice_list]
            elif type(seq) is int:
                return self.get_file_list(self.sequence_list[seq])

        else:
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

    def get_z_coords(self, seq, use_v3=False):
        if not (CFG.get_testing_status("use-slice-location") or use_v3):
            return []

        con = sqlite3.connect(CFG.get_db())

        if type(seq) is str:
            query = f"""
                     select distinct slice_location from slice_locations
                     inner join sequence_files
                     on sequence_files.file_id = slice_locations.file_id
                     inner join sequences
                     on sequences.seq_id = sequence_files.seq_id
                     where sequences.name = '{seq}'
                     and sequence_files.case_id = {self.case_id}
                     order by slice_location desc;
                     """
            z_list = [float(item[0]) for item in con.cursor().execute(query).fetchall()]
            con.close()
            return sorted(z_list)
        elif type(seq) is int:
            return self.get_z_coords(self.sequence_list[seq])

    def get_image_orientation(self, item) -> ImageOrientation:
        if len(self.get_file_list(item)):
            file = self.get_file_list(item)[0]
            return DICOMImageOrientation.get_image_orientation(file)
        else:
            return ImageOrientation.UNKNOWN

    @staticmethod
    def generate(file_list, use_v3=False):
        """ TempDir dependency is due to an sITK issue, see: https://github.com/SimpleITK/SimpleITK/issues/1609 """
        if CFG.get_testing_status("use-slice-location") or use_v3:
            import pydicom
            import numpy as np

            file_list.sort(key=lambda x: x[1])

            def get_pixel_array(f):
                with open(f, 'rb') as f:
                    ds = pydicom.dcmread(f)
                return ds.pixel_array

            np_out = np.array([get_pixel_array(f) for f, _ in file_list])

            return np_out, [f for f, _ in file_list]
        else:

            reader = sitk.ImageSeriesReader()

            with tempfile.TemporaryDirectory() as temp_dir:
                for fi in file_list:
                    shutil.copy(src=fi, dst=temp_dir)

                dicom_names = reader.GetGDCMSeriesFileNames(temp_dir)
                reader.SetFileNames(dicom_names)
                image = reader.Execute()

            return image
