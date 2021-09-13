import json
import numpy as np
from datetime import datetime, timezone

from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties
from .PointArray import PointArray

import logging
logging.getLogger(__name__)


class SaveFormatter:
    """ handles the formatting and saving of the files """
    def __init__(self, filename, imagedata: ImageProperties):
        self.filename = filename
        self.header = dict(imagedata.header)
        self.output_data = self.header

    def add_pointcollection_data(self, key: str, value: PointArray):
        logging.info(f"added {len(value)} {key} to saved file")
        _points = value.get_coordinates_as_array()

        self.output_data[key] = _points

    def add_generic_data(self, key: str, value):
        """ works for anything except for point collections"""
        logging.info(f"Adding [{key}]: {value}")
        self.output_data[key] = value

    def save_data(self):
        self._clean_data()

        self.output_data['annotation timestamp'] = datetime.now(timezone.utc).astimezone().isoformat()
        with open(self.filename, 'w') as f:
            json.dump(self.output_data, f,
                      indent=4)

    def _clean_data(self):
        for i in self.output_data:
            if type(self.output_data[i]) is np.ndarray:
                self.output_data[i] = self.output_data[i].tolist()
