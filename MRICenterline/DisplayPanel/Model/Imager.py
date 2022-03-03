import os
import sqlite3

import numpy as np
import SimpleITK as sitk
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

from MRICenterline.FileReaders.DICOMReader import DICOMReader
from MRICenterline.FileReaders.NRRDReader import NRRDReader
from MRICenterline.FileReaders import ReadFolder
from .ImageProperties import ImageProperties

from MRICenterline.Config import CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class Imager:
    """
    takes a directory for one case and processes it independent of its reader type so that
    GenericModel can use it for GenericSequenceViewer and other classes
    """
    def __init__(self, directory):
        self.image_list = dict()
        self.case_name = os.path.relpath(directory, CFG.get_folder('raw'))

        self.directory = directory

        self.database_check()
        self.assign_reader()

    ##############################################
    #              public functions              #
    ##############################################

    def get_case_id(self) -> int:
        return self.reader.case_id

    def get_sequences(self) -> list:
        return self.reader.sequence_list

    def get_sequences_and_ids(self) -> tuple:
        return tuple(zip(range(1, len(self)+1), self.reader.sequence_list))

    def __len__(self) -> int:
        return len(self.reader)

    def __getitem__(self, item) -> ImageProperties:
        """
        creates the associated ImageProperties, which contains the sITK image and only the necessary metadata
        to be used by GenericSequenceViewer
        """
        if isinstance(item, int):
            return self[self.get_sequences()[item]]
        else:
            self.sitk_image = self.reader[item]
            self.size = np.array(self.sitk_image.GetSize())
            self.spacing = np.array(self.sitk_image.GetSpacing())
            vtk_data = self.get_vtk_data(self.sitk_image)
            return ImageProperties(vtk_data)

    def get_files(self, seq):
        return self.reader.get_file_list(seq)

    ##############################################
    #             private functions              #
    ##############################################

    @staticmethod
    def get_vtk_data(sitk_image):

        spacing = np.array(sitk_image.GetSpacing())
        size = np.array(sitk_image.GetSize())
        origin = np.array(sitk_image.GetOrigin())
        extent = (0, size[0] - 1,
                  0, size[1] - 1,
                  0, size[2] - 1)

        nparray = sitk.GetArrayFromImage(sitk_image)
        nparray = np.flipud(nparray)
        nparray = np.reshape(nparray, newshape=size)

        vtkVolBase = vtk.vtkImageData()
        vtkVolBase.SetDimensions(*size)
        vtkVolBase.SetOrigin(*origin)
        vtkVolBase.SetSpacing(*spacing)
        vtkVolBase.SetExtent(*extent)

        image_array = numpy_support.numpy_to_vtk(nparray.ravel(), deep=True, array_type=vtk.VTK_TYPE_UINT16)
        vtkVolBase.GetPointData().SetScalars(image_array)
        vtkVolBase.Modified()

        # return vtkVolBase

        # flip the image in Y direction
        flip = vtk.vtkImageReslice()
        flip.SetInputData(vtkVolBase)
        flip.SetResliceAxesDirectionCosines(1, 0, 0, 0, -1, 0, 0, 0, 1)
        flip.Update()

        vtkVol = flip.GetOutput()
        vtkVol.SetOrigin(*origin)

        return vtkVol

    def database_check(self):
        """
        looks for the metadata.db
        checks if it has the case_list table
        and if the case being opened is in the database
        """

        con = sqlite3.connect(CFG.get_db())
        available_cases = [item[0] for item in con.cursor().execute("select case_name from case_list;").fetchall()]

        if self.case_name in available_cases:
            # skips the read_folder part, assigns self.file_type according to what the db says
            logging.debug(f"Found case {self.case_name} in database, reading file type from table")
            execute = con.cursor().execute(f"select * from case_list where case_name='{self.case_name}';").fetchone()

            self.new_case_flag = False
            self.case_id = execute[0]
            # self.case_name = execute[1]
            self.file_type = execute[2]

        else:
            # if missing, send it to the file readers
            self.initialize_folder()
            self.new_case_flag = True

        con.close()

    def assign_reader(self):
        if self.file_type.upper() == "DICOM":
            self.reader = DICOMReader(self.case_id, self.directory, self.new_case_flag)
        elif self.file_type.upper() == "NRRD":
            pass
        else:
            MSG.msg_box_warning("Either that format is not yet implemented or there are no MRI images there.")
            raise NotImplementedError

        logging.debug(f"Assigning reader as {self.file_type}")

    def initialize_folder(self):
        logging.debug("Checking folder type")
        self.file_type = ReadFolder.read_folder(self.directory)
        logging.debug(f"Folder {self.directory} is type {self.file_type}")

        # add the folder to the case_list table
        con = sqlite3.connect(CFG.get_db())
        with con:
            con.execute('insert into case_list (case_name, case_type) values (?, ?)', (self.case_name, self.file_type,))
            self.case_id = con.execute('SELECT max(case_id) FROM case_list').fetchone()[0]
        con.close()








    # def _group_by_type(self):
    #     """
    #     goes through all the items in file_list, checks if the files are nrrd, dicom, or neither
    #     it returns a tuple of lists: dicom, nrrd, where the items in each list is a reader class,
    #     and the list of the folders that have dicom/nrrd files
    #     """
    #     _folder_list = [Path(item)
    #                     for sublist in
    #                     [[os.path.join(root, name) for name in dirs]
    #                      for root, dirs, files in os.walk(self.directory)]
    #                     for item in sublist]
    #
    #     _dicom = list()
    #     _nrrd = list()
    #     _valid_folders = list()
    #
    #     for f in _folder_list:
    #         _dicom_reader = DICOMReader.test_folder(str(f))
    #         _nrrd_reader = None
    #
    #         if _dicom_reader:
    #             _dicom.append(_dicom_reader)
    #             _valid_folders.append(f)
    #         elif _nrrd_reader:
    #             _nrrd.append(_nrrd_reader)
    #             _valid_folders.append(f)
    #
    #     return _dicom, _nrrd, _valid_folders
    #
    # def _process_dicoms(self):
    #     _seq_list = list()
    #     # _image_list = list()
    #     for dicom in self.dicom_list:
    #         for seq in dicom.get_sequence_list():
    #             _seq_list.append(seq)
    #             self.image_list[seq] = Image(dicom, sequence=seq)
    #     return _seq_list
    #
    # def _process_nrrds(self):
    #     _file_list = list()
    #     for nrrd in self.nrrd_list:
    #         pass
    #     return []
    #
    # def __getitem__(self, item):
    #     if isinstance(item, int):
    #         _seq = self.get_sequences()[item]
    #         return self[_seq]
    #     else:
    #         if item not in self.get_sequences():
    #             raise KeyError(f"{item} not found in Imager class")
    #         else:
    #             if item in self.cache.items():
    #                 _window, _level = self.image_list[item].get_window_and_level()
    #                 return ImageProperties(self.cache[item], self.image_list[item].get_header(),
    #                                        window=_window, level=_level,
    #                                        z_coords=self.image_list[item].get_z_coords(),
    #                                        path=self.image_list[item].reader.folder)
    #             else:
    #                 self.cache[item] = self.image_list[item].get_image()
    #                 _window, _level = self.image_list[item].get_window_and_level()
    #                 return ImageProperties(self.cache[item], self.image_list[item].get_header(),
    #                                        window=_window, level=_level,
    #                                        z_coords=self.image_list[item].get_z_coords(),
    #                                        path=self.image_list[item].reader.folder)
    #
    # def get_numpy(self, item):
    #     if isinstance(item, int):
    #         _seq = self.get_sequences()[item]
    #         return self.get_numpy(_seq)
    #     else:
    #         if item not in self.get_sequences():
    #             raise KeyError(f"{item} not found in Imager class")
    #         else:
    #             return self.image_list[item].get_numpy()
    #
    # def get_sequences(self):
    #     return self.sequences + self.files
    #
    # def __len__(self):
    #     return len(self.get_sequences())
    #
    # def get_folders(self):
    #     return self.valid_folders

#
# class Image:
#     """ translates any reader and flattens it to one vtkImageData volume """
#     def __init__(self, reader, **kwargs):
#         self.reader = reader
#         self._check_kwargs(kwargs)
#
#     def _check_kwargs(self, kwargs):
#         if isinstance(self.reader, DICOMReader):
#             if 'sequence' not in kwargs:
#                 raise AttributeError("Sequence required for DICOM")
#             else:
#                 self._type = 'dicom'
#                 self._param = kwargs['sequence']
#
#         elif isinstance(NRRDReader, self.reader):
#             if 'filename' not in kwargs:
#                 raise AttributeError("Filename required for NRRD")
#             else:
#                 self._type = 'nrrd'
#                 self._param = kwargs['filename']
#         else:
#             self._type = 'empty'
#
#     def _process_single_dicom(self, sequence):
#         self._vtkImageData_array = self.reader.convert_to_vtk(sequence)
#         self.header = self.reader.get_header(sequence)
#         self.window, self.level = self.reader.get_window_and_level(sequence)
#         self.z_coords = self.reader.get_z_coords_list(sequence)
#
#     def get_numpy(self):
#         return self.reader.get_numpy(self._param)
#
#     def get_image(self) -> vtkImageData:
#         """ the items are the slices """
#         if self._type == 'dicom':
#             self._process_single_dicom(self._param)
#             return self._vtkImageData_array
#         elif self._type == "nrrd":
#             pass
#         elif self._type == 'empty':
#             return vtkImageData()
#         else:
#             logging.critical("Bad type in Image class.")
#             raise NotImplementedError("Issue with Image class. Please notify developers.")
#
#     def get_header(self):
#         return self.header
#
#     def get_window_and_level(self):
#         return self.window, self.level
#
#     def get_z_coords(self):
#         return self.z_coords
