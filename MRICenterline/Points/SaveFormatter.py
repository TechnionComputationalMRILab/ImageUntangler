import json
import numpy as np

from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties
from .PointCollection import PointCollection

import logging
logging.getLogger(__name__)

ACCEPTABLE_FILE_TYPES = ['csv', 'json', 'sqllite', 'mysql', 'hdf5']
NOT_IMPLEMENTED = ['csv', 'sqllite', 'mysql', 'hdf5']


class SaveFormatter:
    """ handles the formatting and saving of the files """
    def __init__(self, filename, imagedata: ImageProperties):
        self.filename = filename
        self.header = dict(imagedata.header)
        self.output_data = self.header

    def add_pointcollection_data(self, key: str, value: PointCollection):
        logging.info(f"added {len(value)} {key} to saved file")
        _points = value.getCoordinatesArray()[:, 0:3]

        self.output_data[key] = _points

    def add_generic_data(self, key: str, value):
        logging.info(f"Adding [{key}]: {value}")
        """ works for anything except for point collections"""
        self.output_data[key] = value

    # def add_sliceidx_list(self, key, value):
    #     logging.info(f"Adding {len(value)} slice indices to saved file")
    #     self.output_data[key + " sliceIdx_list"] = value

    def save_data(self):
        self._clean_data()
        with open(self.filename, 'w') as f:
            json.dump(self.output_data, f,
                      indent=4)

    def _clean_data(self):
        for i in self.output_data:
            if type(self.output_data[i]) is np.ndarray:
                self.output_data[i] = self.output_data[i].tolist()
