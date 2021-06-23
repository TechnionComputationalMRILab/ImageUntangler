from NRRDReader import NRRDReader
from DICOMReader import DICOMReader
import os
from tqdm import tqdm
from icecream import ic
from vtkmodules.all import vtkImageData
from vtk.util import numpy_support


class Imager:
    def __init__(self, directory):
        self.directory = directory
        self.dicom_list, self.nrrd_list = self._group_by_type()

        if len(self.dicom_list):
            self._process_dicoms()
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

        _dicom = list()
        _nrrd = list()
        for f in tqdm(_folder_list):

            _dicom_reader = DICOMReader.test_folder(f)
            _nrrd_reader = None

            if _dicom_reader:
                _dicom.append(_dicom_reader)
            elif _nrrd_reader:
                _nrrd.append(_nrrd_reader)

        return _dicom, _nrrd

    def _process_dicoms(self):
        for dicom in self.dicom_list:
            pass

    def _process_nrrds(self):
        for nrrd in self.nrrd_list:
            pass


class Image:
    # TODO
    def __init__(self, reader, **kwargs):
        self.x_points = list()
        self.y_points = list()
        self.z_points = list()

        self.reader = reader
        self._check_kwargs(kwargs)

    def _check_kwargs(self, kwargs):
        if isinstance(DICOMReader, self.reader):
            if 'sequence' not in kwargs:
                raise AttributeError("Sequence required for DICOM")
            else:
                self._process_single_dicom(kwargs['sequence'])

        elif isinstance(NRRDReader, self.reader):
            if 'filename' not in kwargs:
                raise AttributeError("Filename required for NRRD")
            else:
                pass

    def _process_single_dicom(self, sequence):
        self.z_points = [z[0] for z in self.reader[sequence]]


if __name__ == "__main__":
    a = Imager('C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\')
    for i in a.dicom_list:
        ic(i)
