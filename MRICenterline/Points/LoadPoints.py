import json
import os
# from icecream import ic
from .PointCollection import PointCollection

import logging
logging.getLogger(__name__)


class LoadPoints:
    def __init__(self, filename, image_data):
        self.filename = filename
        self.image_data = image_data
        self.slide_indices = []

        self.points = PointCollection()
        self._open_file()

    def _calculate_slideIdx(self, point):
        return self.image_data.convertZCoordsToSlices([point])[0]

    def get_points(self): # -> PointCollection:
        logging.debug(f"Getting point data from {self.filename}")
        _point_type = self._get_type_of_points()

        logging.info(f"Loading {len(self.json_data[_point_type])} {_point_type}")
        for i in self.json_data[_point_type]:
            self.slide_indices.append(self._calculate_slideIdx(i[2]))
            i.append(self._calculate_slideIdx(i[2]))
            self.points.addPoint(i)
        return self.points

    def _get_type_of_points(self):
        if "length points" in self.json_data.keys():
            logging.debug("Opened length points JSON file")
            return "length points"
        elif "MPR points" in self.json_data.keys():
            logging.debug("Opened MPR points JSON file")
            return "MPR points"
        elif "length in mpr points" and "mpr points" in self.json_data.keys():
            print("length in mpr points open")
            logging.debug("Opened length points in MPR JSON file")
        else:
            logging.error("JSON file invalid, point headers not found")
            return None

    def _open_file(self):
        with open(self.filename, 'r') as f:
            logging.info(f"Opening annotation from {self.filename}")
            self.json_data = json.load(f)
