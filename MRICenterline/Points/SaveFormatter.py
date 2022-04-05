import os
import json
import csv
import numpy as np
from datetime import datetime, timezone, timedelta
from pathlib import Path

from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties
from MRICenterline.Points import PointArray

from MRICenterline.utils import message as MSG
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class SaveFormatter:
    """ handles the formatting and saving of the files """
    def __init__(self, imagedata: ImageProperties, path, prefix: str = "",
                 append_to_directory=True, use_data_folder=True):
        self.path = Path(path)
        self.imagedata = imagedata
        self.append_to_directory = append_to_directory
        self.filename = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y__%H_%M") + "." + prefix + ".annotation"
        self.case_number = os.path.basename(self.path)

        if use_data_folder:
            self.save_to = os.path.join(path, 'data')
        else:
            self.save_to = path

        self.header = dict(imagedata.header)

        self.output_data = self.header
        self.output_data['annotation timestamp'] = datetime.now(timezone.utc).astimezone().isoformat()
        self.output_data['VERSION_NUMBER'] = CONST.VER_NUMBER

    def add_pointcollection_data(self, key: str, value: PointArray):
        logging.info(f"added {len(value)} {key} to saved file")
        _points = value.get_coordinates_as_array()

        self.output_data[key] = _points

    def add_generic_data(self, key: str, value):
        """ works for anything except for point collections"""
        logging.info(f"Adding generic-formatting data {key}")
        self.output_data[key] = value

    def add_timestamps(self, start_time=None, stop_time=None, time_gap=None):
        if start_time and not stop_time:
            logging.info("Setting the stop_time as the current timestamp.")
            stop_time = datetime.now(timezone.utc).astimezone()
            self.output_data['START'] = start_time.isoformat()
            self.output_data['STOP'] = stop_time.isoformat()

            if time_gap:
                all_gaps = sum(time_gap, timedelta())
                self.output_data['Time measurement'] = str(stop_time - start_time - all_gaps)
            else:
                self.output_data['Time measurement'] = str(stop_time - start_time)

        elif start_time and stop_time:
            logging.debug("Saving with provided start and stop timestamp.")
            self.output_data['START'] = start_time.isoformat()
            self.output_data['STOP'] = stop_time.isoformat()
            self.output_data['Time measurement'] = str(stop_time - start_time)

            if time_gap:
                all_gaps = sum(time_gap, timedelta())
                self.output_data['Time measurement'] = str(stop_time - start_time - all_gaps)
            else:
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
        with open(os.path.join(self.save_to, self.filename + ".json"), 'w') as f:
            json.dump(self.output_data, f,
                      indent=4)

        if self.append_to_directory:
            self._append_to_directory()
        MSG.msg_box_info(f"Save completed to {self.filename}!")

    def _append_to_directory(self):
        _directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'directory.csv')
        _num_of_mpr_points = len(self.output_data['MPR points']) if "MPR points" in self.output_data.keys() else 0
        _num_of_len_points = len(self.output_data['length points']) if "length points" in self.output_data.keys() else 0

        with open(_directory, 'a', newline='') as f:
            _writer = csv.writer(f)

            # ['case number', 'sequence name', 'date', '# MPR points', '# len points',
                                        #   'Time measurement', 'length', 'path', 'filename']
            _writer.writerow([self.case_number,
                              self.output_data['SeriesDescription'],
                              datetime.now(timezone.utc).astimezone().strftime('%d.%m.%Y %H:%M'),
                              _num_of_mpr_points,
                              _num_of_len_points,
                              self.output_data['Time measurement'],
                              round(0, 2),
                              self.save_to,
                              self.filename + ".json"])

    def _clean_data(self):
        def transform(pts):
            viewerOrigin = [i / 2 for i in self.imagedata.dimensions]

            coords_arr_numpy = np.zeros(pts.shape)
            for i, coords in enumerate(pts):
                imageCoords = np.zeros(3, dtype=np.int32)
                imageCoords[0] = round(coords[0] / self.imagedata.spacing[0] + viewerOrigin[0])
                imageCoords[1] = round(self.imagedata.dimensions[1] - (coords[1] / self.imagedata.spacing[1] + viewerOrigin[1]))
                imageCoords[2] = np.argmin(np.abs(self.imagedata.z_coords - coords[2]))

                coords_arr_numpy[i, :] = imageCoords

            return coords_arr_numpy

        npzdict = self.output_data.copy()
        for k, v in self.output_data.items():
            if type(v) is np.ndarray:
                npzdict[k] = transform(v)
        np.savez(file=os.path.join(self.save_to, self.filename), **npzdict)

        for i in self.output_data:
            if type(self.output_data[i]) is np.ndarray:
                self.output_data[i] = self.output_data[i].tolist()
