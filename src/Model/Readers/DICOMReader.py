import pydicom
from typing import List
import numpy as np


class DICOMReader:
    def __init__(self, MRIimages: List[str]):
        self.mri_images = MRIimages

    def _group_sequence_by_name(self):
        """
        looks at the mri_images property, gets the series description for
        each image, then takes the series descriptions and attaches each
        desc to each filename.

        returns a dictionary with the keys as the series descriptions and
        the values as a list of the filenames with that series desc
        """
        _images_and_series_desc = self.mri_images.copy()

        for i, s in enumerate(_images_and_series_desc):
            _images_and_series_desc[i] = self._get_series_description(s)

        _sequences = list(set(_images_and_series_desc))
        _images_and_series_desc = np.stack([self.mri_images, _images_and_series_desc], axis=1)
        _grouped_sequences = [_images_and_series_desc[_images_and_series_desc[:, -1] == seq][:, 0]
                              for seq in _sequences]
        _sequence_dict = {v: list(_grouped_sequences[k]) for k, v in enumerate(_sequences)}

        return _sequence_dict

    @staticmethod
    def _get_series_description(filename):
        """
        uses the pydicom module to get the series description. can be
        easily adapted to get other header data. see pydicom documentation
        """
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        return ds.SeriesDescription

    @staticmethod
    def _get_generic_info(header_name, filename):
        """
        uses pydicom's dir() method to get additional information from the header
        ex: header_name = 'patient' returns a dict with all keys with the word
        'patient' in it
        """
        with open(filename, 'rb') as f:
            ds = pydicom.dcmread(f)
        return {i: ds[i].value for i in ds.dir(header_name)}
