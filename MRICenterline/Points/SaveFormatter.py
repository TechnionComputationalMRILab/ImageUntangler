import os
import json
import csv
import numpy as np
from datetime import datetime, timezone

from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties
from MRICenterline.Points import PointArray

from MRICenterline.utils import message as MSG
from MRICenterline.Config import ConfigParserRead as CFG

import logging
logging.getLogger(__name__)


class SaveFormatter:
    """ handles the formatting and saving of the files """
    def __init__(self, imagedata: ImageProperties):
        self.filename = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y__%H_%M") + ".annotation.json"
        self.case_number = [int(s) for s in os.path.dirname(imagedata.header['filename'][-1]).split("/") if s.isdigit()][-1]
        self.save_to = os.path.join(os.path.dirname(imagedata.header['filename'][-1]), 'data')
        self.header = dict(imagedata.header)

        self.output_data = self.header
        self.output_data['annotation timestamp'] = datetime.now(timezone.utc).astimezone().isoformat()

    def add_pointcollection_data(self, key: str, value: PointArray):
        logging.info(f"added {len(value)} {key} to saved file")
        _points = value.get_coordinates_as_array()

        self.output_data[key] = _points

    def add_generic_data(self, key: str, value):
        """ works for anything except for point collections"""
        logging.info(f"Adding [{key}]: {value}")
        self.output_data[key] = value

    def add_timestamps(self, start_time=None, stop_time=None):
        if start_time and not stop_time:
            logging.info("Setting the stop_time as the current timestamp.")
            stop_time = datetime.now(timezone.utc).astimezone()
            self.output_data['START'] = start_time.isoformat()
            self.output_data['STOP'] = stop_time.isoformat()
            self.output_data['Time measurement'] = str(stop_time - start_time)

        elif start_time and stop_time:
            logging.debug("Saving with provided start and stop timestamp.")
            self.output_data['START'] = start_time.isoformat()
            self.output_data['STOP'] = stop_time.isoformat()
            self.output_data['Time measurement'] = str(stop_time - start_time)

        else:
            logging.debug("Not start/stop entered")
            self.output_data['START'] = " "
            self.output_data['STOP'] = " "
            self.output_data['Time measurement'] = " "

        logging.info(f"Time elapsed: {self.output_data['Time measurement']}")

    def save_data(self):
        self._clean_data()
        logging.info(f"Saving to {os.path.join(self.save_to, self.filename)}")
        with open(os.path.join(self.save_to, self.filename), 'w') as f:
            json.dump(self.output_data, f,
                      indent=4)

        self._append_to_directory()
        MSG.msg_box_info(f"Save complete!")

    def _append_to_directory(self):
        _directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'directory.csv')
        _num_of_mpr_points = len(self.output_data['MPR points']) if "MPR points" in self.output_data.keys() else 0
        with open(_directory, 'a', newline='') as f:
            _writer = csv.writer(f)

            # ['case number', 'sequence name', 'date', 'number of MPR points', 'path', 'filename']
            _writer.writerow([self.case_number,
                              self.output_data['SeriesDescription'],
                              datetime.now(timezone.utc).astimezone().strftime('%d.%m.%Y %H:%M'),
                              _num_of_mpr_points,
                              self.save_to,
                              self.filename])

    def _clean_data(self):
        for i in self.output_data:
            if type(self.output_data[i]) is np.ndarray:
                self.output_data[i] = self.output_data[i].tolist()
