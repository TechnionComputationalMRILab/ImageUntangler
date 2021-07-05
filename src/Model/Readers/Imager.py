import os, psutil

from Model.Readers.DICOMReader import DICOMReader
from Model.Readers.NRRDReader import NRRDReader
from tqdm import tqdm
from icecream import ic
from vtkmodules.all import vtkImageData
from scipy.stats import mode

from util import ConfigRead as CFG, logger
logger = logger.get_logger()
ic.configureOutput(includeContext=True)


class Imager:
    def __init__(self, directory):
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
        _key_list = list()

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
        # _image_list = list()
        for dicom in self.dicom_list:
            for seq in dicom.get_sequence_list():
                _seq_list.append(seq)
                # _image_list.append(Image(dicom, sequence=seq))
        return _seq_list

    def _process_nrrds(self):
        _file_list = list()
        for nrrd in self.nrrd_list:
            pass
        return []

    def __getitem__(self, item):
        if item not in self.get_sequences():
            raise KeyError(f"{item} not found in Imager class")
        else:
            if item in self.cache.items():
                return self.cache[item]
            else:
                self.cache[item] = dict() # TODO: generate the image
                return self.cache[item]

    def get_sequences(self):
        return self.sequences + self.files

    def get_folders(self):
        return self.valid_folders

    def get_keys(self):
        return ()  # folder and filename/sequence


class Image:
    """ translates any reader and flatten it to one vtkImageData volume """
    def __init__(self, reader, **kwargs):
        self.reader = reader
        self._check_kwargs(kwargs)

    def _check_kwargs(self, kwargs):
        if isinstance(self.reader, (DICOMReader)):
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
        _x_spacing = 1
        _y_spacing = 1

        if CFG.get_testing_status('ignore-uneven-slices'):
            _z_spacing = mode([round(z[0]) for z in self.reader[sequence]])
        else:
            _rounded_z = [round(z[0]) for z in self.reader[sequence]]
            _dz = [_rounded_z[i-1] - _rounded_z[i] for i in range(1, len(_rounded_z))]
            if len(set(_dz)) > 1:
                raise ValueError("z-spacing not equal between slices")
            else:
                _z_spacing = set(_dz)

        self._vtkImageData_array = self.reader.convert_to_vtk(sequence, spacing=(_x_spacing, _y_spacing, _z_spacing))

    def __getitem__(self, item) -> vtkImageData:
        """ the items are the slices """
        if self._type == 'dicom':
            self._process_single_dicom(self._param)
            return self._vtkImageData_array[item]
        elif self._type == "nrrd":
            pass
        elif self._type == 'empty':
            return vtkImageData()
        else:
            logger.critical("Bad type in Image class.")
            raise NotImplementedError("Issue with Image class. Please notify developers.")


if __name__ == "__main__":
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    a = Imager('C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data')

    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print(a.get_keys())

    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
