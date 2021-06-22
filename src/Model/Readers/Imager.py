from NRRDReader import NRRDReader
from DICOMReader import DICOMReader
import os
from tqdm import tqdm
from nrrd import read_header
from pydicom import dcmread


class Imager:
    """
    looks at a directory, figures out the folder structure, identifies which reader to use
    and then converts the pixel data from the reader to vtkImageData
    """
    def __init__(self, directory):
        self.directory = directory
        # self.dicom_list, self.nrrd_list = self._group_by_type()
        #
        # if len(self.dicom_list):
        #     self._process_dicom()
        # if len(self.nrrd_list):
        #     self._process_nrrd()

    def _group_by_type(self):
        """
        goes through all the items in file_list, checks if the files are nrrd, dicom, or neither
        it returns a tuple of lists: dicom_folders, nrrd_folders
        """
        _folder_list = [item
                        for sublist in
                            [[os.path.join(root, name) for name in dirs]
                             for root, dirs, files in os.walk(self.directory)]
                        for item in sublist]

        _dicom_folders = list()
        _nrrd_folders = list()
        for i in tqdm(_folder_list):
            if self.has_valid_dicom(str(i)):
                _dicom_folders.append(i)
            elif self.has_valid_nrrd(str(i)):
                _nrrd_folders.append(i)

        return _dicom_folders, _nrrd_folders

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
    def has_valid_nrrd(folder):
        try:
            with open(filename, 'rb') as infile:
                read_header(infile)
        except:
            return False
        else:
            return True

    @staticmethod
    def has_valid_dicom(folder):
        try:
            with open(filename, 'rb') as infile:
                dcmread(infile)
        except:
            return False
        else:
            return True


if __name__ == "__main__":
    a = Imager('C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\')
    a._group_by_type()
