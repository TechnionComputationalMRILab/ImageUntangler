import pydicom
from typing import List
import numpy as np


class DICOMReader:
    def __init__(self, MRIimages: List[str]):
        self.mri_images = MRIimages
        self.sequence_dict = self._groupby(lambda x: self._get_info('SeriesDescription', x))
        self.patient_dict = self._groupby(lambda x: self._get_info('PatientName', x))

    def _groupby(self, func):
        _images_and_series_desc = self.mri_images.copy()

        for i, s in enumerate(_images_and_series_desc):
            _images_and_series_desc[i] = func(s)

        _sequences = list(set(_images_and_series_desc))
        _images_and_series_desc = np.stack([self.mri_images, _images_and_series_desc], axis=1)
        _grouped_sequences = [_images_and_series_desc[_images_and_series_desc[:, -1] == seq][:, 0]
                              for seq in _sequences]
        _sequence_dict = {v: list(_grouped_sequences[k]) for k, v in enumerate(_sequences)}

        return _sequence_dict

    @staticmethod
    def _get_info(header_name, filename, get_one=True):
        """
        uses pydicom's dir() method to get additional information from the header
        ex: header_name = 'patient' returns a dict with all keys with the word
        'patient' in it
        """
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        if get_one:
            return str(ds[header_name].value)
        else:
            return {i: ds[i].value for i in ds.dir(header_name)}

    @staticmethod
    def _get_pixel_array(filename):
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        return ds.pixel_array

    def get_sequence_dict(self):
        """
        returns a dict with the sequence name and the files linked to that
        sequence
        """
        return self.sequence_dict

    def get_patient_dict(self):
        """
        returns a dict with the patient name and the files associated with
        the patient
        """
        return self.patient_dict

    def get_pixel_data(self, sequence):
        _list_of_files = self.sequence_dict[sequence]

        _tuple_list = list(zip(#_list_of_files,
                               [float(self._get_info('SliceLocation', f)) for f in _list_of_files],
                               [self._get_pixel_array(f) for f in _list_of_files]))
        _tuple_list.sort(key=lambda x: x[0])
        return _tuple_list


def get_images_from_folder(l):
    from os import walk
    f = []
    for (dir_path, dir_names, filenames) in walk(l):
        f.extend(filenames)
        break
    return f


if __name__ == "__main__":
    path = "C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\enc_files\\"
    list_of_files = get_images_from_folder(path)
    a = DICOMReader([path + i for i in list_of_files])

    # print(a.get_sequence_dict().keys())

    print(a.get_pixel_data('Cor T2 SSFSE'))
