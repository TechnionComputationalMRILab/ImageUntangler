import json
import os
from icecream import ic
from MainWindowComponents import MessageBoxes
from Model.PointCollection import PointCollection
from util import logger
logger = logger.get_logger()
ic.configureOutput(includeContext=True)

class PointLoader:
    def __init__(self, filename, image_data):
        self.filename = filename
        self.image_data = image_data
        self.slide_indices = []

        self.points = PointCollection()
        self._open_file()

    def _calculate_slideIdx(self, point):
        return self.image_data.convertZCoordsToSlices([point])[0]

    def get_points(self): # -> PointCollection:
        logger.debug(f"Getting point data from {self.filename}")
        _point_type = self._get_type_of_points()

        logger.info(f"Loading {len(self.json_data[_point_type])} {_point_type}")
        for i in self.json_data[_point_type]:
            self.slide_indices.append(self._calculate_slideIdx(i[2]))
            i.append(self._calculate_slideIdx(i[2]))
            self.points.addPoint(i)
        return self.points

    def _get_type_of_points(self):
        if "length points" in self.json_data.keys():
            logger.debug("Opened length points JSON file")
            return "length points"
        elif "MPR points" in self.json_data.keys():
            logger.debug("Opened MPR points JSON file")
            return "MPR points"
        elif "length in mpr points" and "mpr points" in self.json_data.keys():
            print("length in mpr points open")
            logger.debug("Opened length points in MPR JSON file")
        else:
            logger.error("JSON file invalid, point headers not found")
            MessageBoxes.json_file_wrong_headers()
            return None

    def _open_file(self):
        with open(self.filename, 'r') as f:
            logger.info(f"Opening {self.filename}")
            self.json_data = json.load(f)

        self._check_metadata()

    def _check_metadata(self):
        """
        get filename of currently viewed file, get filename in header
        throw warning if names are different, but don't close, don't raise an error
        """
        if self.json_data["file type"] == "dicom":
            """ compare patient ID """
            pass
        else:
            if os.path.basename(self.json_data['filename']).upper() == os.path.basename(self.image_data.header["filename"]).upper():
                pass
            else:
                MessageBoxes.file_mismatch_warning()
                logger.warning(f"Filename in loaded JSON file does not match currently opened file")
