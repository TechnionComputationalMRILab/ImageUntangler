import os
from vtkmodules.all import vtkImageData

from MRICenterline.FileReaders.DICOMReader import DICOMReader
from MRICenterline.FileReaders.NRRDReader import NRRDReader
from .ImageProperties import ImageProperties

import logging
logging.getLogger(__name__)


class Imager:
    def __init__(self, directory):
        self.image_list = dict()

        self.directory = directory
        self.dicom_list, self.nrrd_list, self.valid_folders = self._group_by_type()

        self.cache = {k: vtkImageData() for k in self.valid_folders}

        self.sequences = self._process_dicoms() if len(self.dicom_list) else list()
        self.files = self._process_nrrds() if len(self.nrrd_list) else list()

    def _group_by_type(self):
        """
        goes through all the items in file_list, checks if the files are nrrd, dicom, or neither
        it returns a tuple of lists: dicom, nrrd, where the items in each list is a reader class,
        and the list of the folders that have dicom/nrrd files
        """
        _folder_list = [item
                        for sublist in
                            [[os.path.join(root, name) for name in dirs]
                             for root, dirs, files in os.walk(self.directory)]
                        for item in sublist]
        _folder_list.append(self.directory)

        _dicom = list()
        _nrrd = list()
        _valid_folders = list()

        for f in _folder_list:
            _dicom_reader = DICOMReader.test_folder(f)
            _nrrd_reader = None

            if _dicom_reader:
                _dicom.append(_dicom_reader)
                _valid_folders.append(f)
            elif _nrrd_reader:
                _nrrd.append(_nrrd_reader)
                _valid_folders.append(f)

        return _dicom, _nrrd, _valid_folders

    def _process_dicoms(self):
        _seq_list = list()
        _image_list = list()
        for dicom in self.dicom_list:
            for seq in dicom.get_sequence_list():
                _seq_list.append(seq)
                # _image_list.append(Image(dicom, sequence=seq))
                self.image_list[seq] = Image(dicom, sequence=seq)
        return _seq_list

    def _process_nrrds(self):
        _file_list = list()
        for nrrd in self.nrrd_list:
            pass
        return []

    def __getitem__(self, item):
        if isinstance(item, int):
            _seq = self.get_sequences()[item]
            return self[_seq]
        else:
            if item not in self.get_sequences():
                raise KeyError(f"{item} not found in Imager class")
            else:
                if item in self.cache.items():
                    _window, _level = self.image_list[item].get_window_and_level()
                    return ImageProperties(self.cache[item], self.image_list[item].get_header(),
                                           window=_window, level=_level,
                                           z_coords=self.image_list[item].get_z_coords())
                else:
                    self.cache[item] = self.image_list[item].get_image()
                    _window, _level = self.image_list[item].get_window_and_level()
                    return ImageProperties(self.cache[item], self.image_list[item].get_header(),
                                           window=_window, level=_level,
                                           z_coords=self.image_list[item].get_z_coords())

    def get_sequences(self):
        return self.sequences + self.files

    def __len__(self):
        return len(self.get_sequences())

    def get_folders(self):
        return self.valid_folders


class Image:
    """ translates any reader and flattens it to one vtkImageData volume """
    def __init__(self, reader, **kwargs):
        self.reader = reader
        self._check_kwargs(kwargs)

    def _check_kwargs(self, kwargs):
        if isinstance(self.reader, DICOMReader):
            if 'sequence' not in kwargs:
                raise AttributeError("Sequence required for DICOM")
            else:
                self._type = 'dicom'
                self._param = kwargs['sequence']

        elif isinstance(NRRDReader, self.reader):
            if 'filename' not in kwargs:
                raise AttributeError("Filename required for NRRD")
            else:
                self._type = 'nrrd'
                self._param = kwargs['filename']
        else:
            self._type = 'empty'

    def _process_single_dicom(self, sequence):
        self._vtkImageData_array = self.reader.convert_to_vtk(sequence)
        self.header = self.reader.get_header(sequence)
        self.window, self.level = self.reader.get_window_and_level(sequence)
        self.z_coords = self.reader.get_z_coords_list(sequence)

    def get_image(self) -> vtkImageData:
        """ the items are the slices """
        if self._type == 'dicom':
            self._process_single_dicom(self._param)
            return self._vtkImageData_array
        elif self._type == "nrrd":
            pass
        elif self._type == 'empty':
            return vtkImageData()
        else:
            logging.critical("Bad type in Image class.")
            raise NotImplementedError("Issue with Image class. Please notify developers.")

    def get_header(self):
        return self.header

    def get_window_and_level(self):
        return self.window, self.level

    def get_z_coords(self):
        return self.z_coords
