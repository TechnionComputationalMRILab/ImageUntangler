import json
# from icecream import ic
from MRICenterline.Points import PointArray, Point

import logging
logging.getLogger(__name__)


class LoadPoints:
    def __init__(self, filename, image_data):
        self.filename = filename
        self.image_data = image_data

        self.slide_indices = []

        self._open_file()
        self.point_set = self.get_points()

    def _calculate_slideIdx(self, point):
        return self.image_data.convertZCoordsToSlices([point])[0]

    def get_points(self): # -> PointArray:
        logging.debug(f"Getting point data from {self.filename}")
        _point_type = self._get_type_of_points()

        _ptset = {}
        for point_set in _point_type:
            logging.info(f"Loading {len(self.json_data[point_set])} {point_set} in loader")
            _point_array = PointArray()
            for k, i in enumerate(self.json_data[point_set]):
                _point = Point(i + [self._calculate_slideIdx(i[2])])
                self.slide_indices.append(self._calculate_slideIdx(i[2]))
                _point_array.add_point(_point)
            _ptset[point_set] = _point_array
        return _ptset

    def _get_type_of_points(self):
        if "length points" in self.json_data.keys() and "MPR points" in self.json_data.keys():
            logging.debug("Opening MPR and length points")
            return ["length points", "MPR points"]
        elif "length points" in self.json_data.keys():
            logging.debug("Opened length points JSON file")
            return ["length points"]
        elif "MPR points" in self.json_data.keys():
            logging.debug("Opened MPR points JSON file")
            return ["MPR points"]
        elif "length in mpr points" and "mpr points" in self.json_data.keys():
            logging.debug("Opened length points in MPR JSON file")
            raise NotImplemented
        else:
            logging.error("JSON file invalid, point headers not found")
            return None

    def _open_file(self):
        with open(self.filename, 'r') as f:
            logging.info(f"Opening annotation from {self.filename}")
            self.json_data = json.load(f)
