from NRRDReader import NRRDReader
from DICOMReader import DICOMReader
import os
from tqdm import tqdm
from nrrd import read_header
from pydicom import dcmread


class Imager:
    """
    looks at a directory, figures out the folder structure, what files are inside,
    and then generates a list of Image objects (see below) for all sequences in the folder.
    returns vtkactors for use in control.
    """
    def __init__(self, directory):
        self.directory = directory
        self.dicom_list, self.nrrd_list = self._group_by_type()

        if len(self.dicom_list):
            self._process_dicom()
        if len(self.nrrd_list):
            self._process_nrrd()

    def _group_by_type(self):
        """
        goes through all the items in file_list, checks if the files are nrrd, dicom, or neither
        and creates a list of tuples: (path+filename, is_dicom, is_nrrd).
        and then, from that tuple-list, it returns a tuple of lists: dicom_files, nrrd_files
        """
        _file_list = [[os.path.join(root, name) for name in files] for root, dirs, files in os.walk(self.directory)]
        _flat_file_list = [item for sublist in _file_list for item in sublist]

        _dicom_files = list()
        _nrrd_files = list()
        for i in tqdm(_flat_file_list):
            if self.is_valid_dicom(str(i)):
                _dicom_files.append(i)
            elif self.is_valid_nrrd(str(i)):
                _nrrd_files.append(i)

        return _dicom_files, _nrrd_files

    def _process_nrrd(self):
        pass

    def _process_dicom(self):
        _dicom_reader = DICOMReader(self.dicom_list)

        if len(_dicom_reader.get_patient_dict().keys()) == 1:
            for keys in _dicom_reader.get_sequence_dict().keys():
                Image(_dicom_reader.get_sequence_dict()[keys])
            print(len(_dicom_reader.get_sequence_dict().keys()))
        else:
            raise NotImplementedError("Cannot handle multiple patients in one directory.")

    def get_vtk(self):
        pass

    @staticmethod
    def is_valid_nrrd(filename: str):
        try:
            with open(filename, 'rb') as infile:
                read_header(infile)
        except:
            return False
        else:
            return True

    @staticmethod
    def is_valid_dicom(filename: str):
        try:
            with open(filename, 'rb') as infile:
                dcmread(infile)
        except:
            return False
        else:
            return True


class Image:
    """ holds the pixel array and the ImageProperties of one sequence """
    def __init__(self, files):
        self.file = files



if __name__ == "__main__":
    Imager('C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\enc_files')
