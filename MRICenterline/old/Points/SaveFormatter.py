import os
import sqlite3
import csv
import numpy as np
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

from MRICenterline.DisplayPanel.Model.Imager import Imager
from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties
from MRICenterline.Points import PointArray, Point

from MRICenterline.utils import message as MSG
from MRICenterline.Config import CFG
from MRICenterline.utils import program_constants as CONST

import logging
logging.getLogger(__name__)


class SaveFormatter:
    """ handles the formatting and saving of the files """
    # def __init__(self, imagedata: ImageProperties, path, suffix: str = "",
    #              append_to_directory=True, use_data_folder=True):
    def __init__(self, parent, imager: Imager):
        self.mpr_points: List[Point] = parent.MPRpoints.physical_points
        self.length_points: List[Point] = parent.lengthPoints.physical_points
        self.display_seq_id: int = parent.manager.seq_idx + 1
        self.case_id: int = imager.get_case_id()
        self.sitk_image = imager[parent.manager.seq_idx].sitk_image
        self.time_gap = 0

        self._session_id = -1

    def __repr__(self):
        return f"""
        Saving {len(self.length_points)} length points, {len(self.mpr_points)} MPR points
        on case [{self.case_id}] and seq [{self.display_seq_id}]
        """

    def set_time_gap(self, time_gap: int = 0):
        self.time_gap = time_gap

    def save(self):
        timestamp = datetime.now(timezone.utc).astimezone().strftime(CONST.TIMESTAMP_FORMAT)

        con = sqlite3.connect(CFG.get_db())

        logging.debug(f"Inserting {len(self.length_points)} length points")
        if len(self.length_points):
            lengths_id = con.cursor().execute("""
                                              select count(*) 
                                              from (
                                                  select distinct lengths_id 
                                                  from 'length_coordinates'
                                                  )""").fetchone()[0] + 1
            for pt in self.length_points:
                with con:
                    con.execute("""insert into 'length_coordinates'
                                   (lengths_id, x, y, z)
                                   values
                                   (?, ?, ?, ?)
                                """,
                                (lengths_id, *pt))
        else:
            lengths_id = None

        logging.debug(f"Inserting {len(self.mpr_points)} MPR points")
        if len(self.mpr_points):
            cl_id = con.cursor().execute("""
                                         select count(*) 
                                         from (
                                             select distinct cl_id
                                             from 'centerline_coordinates'
                                             )""").fetchone()[0] + 1
            for pt in self.mpr_points:
                with con:
                    con.execute("""insert into centerline_coordinates
                                   (cl_id, x, y, z)
                                   values
                                   (?, ?, ?, ?)
                                """,
                                (cl_id, *pt, ))
        else:
            cl_id = None

        session_data = {
            'timestamp': timestamp,
            'time_elapsed_seconds': self.time_gap,
            'lengths_id': lengths_id,
            'cl_id': cl_id,
            'seq_id': self.display_seq_id,
            'case_id': self.case_id
        }

        logging.debug(f"Inserting session data")
        with con:
            con.execute("""insert into sessions 
                           (timestamp, time_elapsed_seconds, lengths_id, cl_id, seq_id, case_id) 
                           values
                           (:timestamp, :time_elapsed_seconds, :lengths_id, :cl_id, :seq_id, :case_id)
                        """,
                        session_data)

        self._session_id = con.cursor().execute("select count(*) from 'sessions'").fetchone()[0]
        con.close()
        logging.info(f"Saved session with id [{self._session_id}] successfully.")

    def overwrite(self):
        pass

    #     self.path = Path(path)
    #     self.append_to_directory = append_to_directory
    #     self.filename = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y__%H_%M") + "." + suffix + ".annotation.json"
    #     self.case_number = os.path.basename(self.path)
    #
    #     if use_data_folder:
    #         self.save_to = os.path.join(path, 'data')
    #     else:
    #         self.save_to = path
    #
    #     self.header = dict(imagedata.header)
    #
    #     self.output_data = self.header
    #     self.output_data['annotation timestamp'] = datetime.now(timezone.utc).astimezone().isoformat()
    #     self.output_data['VERSION_NUMBER'] = CONST.VER_NUMBER
    #
    # def add_pointcollection_data(self, key: str, value: PointArray):
    #     logging.info(f"added {len(value)} {key} to saved file")
    #     _points = value.get_coordinates_as_array()
    #
    #     self.output_data[key] = _points
    #
    # def add_generic_data(self, key: str, value):
    #     """ works for anything except for point collections"""
    #     logging.info(f"Adding generic-formatting data {key}")
    #     self.output_data[key] = value
    #
    # def add_timestamps(self, start_time=None, stop_time=None, time_gap=None):
    #     if start_time and not stop_time:
    #         logging.info("Setting the stop_time as the current timestamp.")
    #         stop_time = datetime.now(timezone.utc).astimezone()
    #         self.output_data['START'] = start_time.isoformat()
    #         self.output_data['STOP'] = stop_time.isoformat()
    #
    #         if time_gap:
    #             all_gaps = sum(time_gap, timedelta())
    #             self.output_data['Time measurement'] = str(stop_time - start_time - all_gaps)
    #         else:
    #             self.output_data['Time measurement'] = str(stop_time - start_time)
    #
    #     elif start_time and stop_time:
    #         logging.debug("Saving with provided start and stop timestamp.")
    #         self.output_data['START'] = start_time.isoformat()
    #         self.output_data['STOP'] = stop_time.isoformat()
    #         self.output_data['Time measurement'] = str(stop_time - start_time)
    #
    #         if time_gap:
    #             all_gaps = sum(time_gap, timedelta())
    #             self.output_data['Time measurement'] = str(stop_time - start_time - all_gaps)
    #         else:
    #             self.output_data['Time measurement'] = str(stop_time - start_time)
    #
    #     else:
    #         logging.debug("Not start/stop entered")
    #         self.output_data['START'] = " "
    #         self.output_data['STOP'] = " "
    #         self.output_data['Time measurement'] = " "
    #
    #     logging.info(f"Time elapsed: {self.output_data['Time measurement']}")
    #
    # def save_data(self):
    #     self._clean_data()
    #     logging.info(f"Saving to {os.path.join(self.save_to, self.filename)}")
    #     with open(os.path.join(self.save_to, self.filename), 'w') as f:
    #         json.dump(self.output_data, f,
    #                   indent=4)
    #
    #     if self.append_to_directory:
    #         self._append_to_directory()
    #     MSG.msg_box_info(f"Save completed to {self.filename}!")
    #
    # def _append_to_directory(self):
    #     _directory = os.path.join(CFG.get_config_data("folders", 'default-folder'), 'directory.csv')
    #     _num_of_mpr_points = len(self.output_data['MPR points']) if "MPR points" in self.output_data.keys() else 0
    #     _num_of_len_points = len(self.output_data['length points']) if "length points" in self.output_data.keys() else 0
    #     _measured_length = round(self.output_data['measured length'], 2) if "measured length" in self.output_data.keys() else 0
    #
    #     with open(_directory, 'a', newline='') as f:
    #         _writer = csv.writer(f)
    #
    #         # ['case number', 'sequence name', 'date', '# MPR points', '# len points',
    #                                     #   'Time measurement', 'length', 'path', 'filename']
    #         _writer.writerow([self.case_number,
    #                           self.output_data['SeriesDescription'],
    #                           datetime.now(timezone.utc).astimezone().strftime('%d.%m.%Y %H:%M'),
    #                           _num_of_mpr_points,
    #                           _num_of_len_points,
    #                           self.output_data['Time measurement'],
    #                           _measured_length,
    #                           os.path.dirname(self.save_to),
    #                           self.filename])
    #
    # def _clean_data(self):
    #     for i in self.output_data:
    #         if type(self.output_data[i]) is np.ndarray:
    #             self.output_data[i] = self.output_data[i].tolist()
