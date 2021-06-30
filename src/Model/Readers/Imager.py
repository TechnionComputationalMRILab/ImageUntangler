import os, psutil

from Model.Readers.DICOMReader import DICOMReader
from Model.Readers.NRRDReader import NRRDReader
from tqdm import tqdm
from icecream import ic
from vtkmodules.all import vtkImageData
from vtkmodules.util import numpy_support

from util import ConfigRead as CFG, logger
logger = logger.get_logger()
ic.configureOutput(includeContext=True)


class Imager:
    def __init__(self, directory):
        self.directory = directory
        self.dicom_list, self.nrrd_list, self.valid_folders = self._group_by_type()

        if len(self.dicom_list):
            self.images, self.sequences = self._process_dicoms()
        if len(self.nrrd_list):
            self._process_nrrds()

    def _group_by_type(self):
        """
        goes through all the items in file_list, checks if the files are nrrd, dicom, or neither
        it returns a tuple of lists: dicom, nrrd, where the items in each list is a reader class
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

        for f in tqdm(_folder_list):
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
                _image_list.append(Image(dicom, sequence=seq))
        return _image_list, _seq_list

    def _process_nrrds(self):
        for nrrd in self.nrrd_list:
            pass

    def get_images(self):
        return self.images

    def get_sequences(self):
        return self.sequences

    def get_folders(self):
        return self.valid_folders


class Image:
    def __init__(self, reader, **kwargs):
        self.reader = reader
        self._check_kwargs(kwargs)

    def _check_kwargs(self, kwargs):
        if isinstance(self.reader, (DICOMReader)):
            if 'sequence' not in kwargs:
                raise AttributeError("Sequence required for DICOM")
            else:
                self._type = 'dicom'
                self._process_single_dicom(kwargs['sequence'])

        elif isinstance(NRRDReader, self.reader):
            if 'filename' not in kwargs:
                raise AttributeError("Filename required for NRRD")
            else:
                self._type = 'nrrd'
                pass

    def _process_single_dicom(self, sequence):
        self.z_points = [z[0] for z in self.reader[sequence]]
        self._vtkImageData_array = self.reader.convert_to_vtk(sequence)

    def __getitem__(self, item):
        """ the items are the slices """
        if self._type == 'dicom':
            return self._vtkImageData_array[item]
        elif self._type == "nrrd":
            pass
        else:
            logger.critical("Bad type in Image class.")
            raise NotImplementedError("Issue with Image class. Please notify developers.")


if __name__ == "__main__":
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    a = Imager('C:\\Users\\ang.a\\OneDrive - Technion\\Documents\\MRI_Data\\enc_files')

    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print(a.get_sequences())

    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)