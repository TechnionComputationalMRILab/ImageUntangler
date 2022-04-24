import os
import json

from MRICenterline import CFG
from MRICenterline.app.points.point import Point
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.status import PointStatus
from MRICenterline.app.points.timer import Timer
from MRICenterline.app.database.save_points import save_points
from MRICenterline.app.database.name_id import get_case_id
from MRICenterline.app.gui_data_handling.slice_loc_based_image_properties import SliceLocImageProperties
from MRICenterline.app.file_reader.dicom.DICOMReader import DICOMReader

import logging
logging.getLogger(__name__)


def timestamp_parse(original: str):
    from datetime import datetime

    split1 = original.split("T")
    date = datetime.strptime(split1[0], "%Y-%m-%d")

    split2 = split1[1].split(".")
    time = datetime.strptime(split2[0], "%H:%M:%S")
    tz = datetime.strptime(split2[1].lstrip("0123456789"), "%z")

    return datetime(date.year, date.month, date.day, hour=time.hour, minute=time.minute, second=time.second,
                    microsecond=0, tzinfo=tz.tzinfo)


class Ver3AnnotationImport:
    def __init__(self, filename, root_folder=None):
        self.filename = filename

        if root_folder:
            self.case_name = os.path.relpath(self.filename.parents[1], root_folder)
        else:
            self.case_name = os.path.relpath(self.filename.parents[1], CFG.get_folder('raw'))

        logging.info(f"Reading file: {self.filename}")

        with open(self.filename, 'r') as f:
            file = json.load(f)

            self.sequence_name = file['SeriesDescription']
            self.timestamp = timestamp_parse(file['annotation timestamp'])

            try:
                self.time_measured = file['Time measurement']
            except KeyError:
                logging.info("No time measured listed")
                self.time_measured = None

            self.mpr_point_array = PointArray(PointStatus.MPR)
            self.length_point_array = PointArray(PointStatus.LENGTH)

            try:
                mpr_coords = file['MPR points']
            except KeyError:
                logging.info(f"Found no MPR points")
            else:
                logging.info(f"Found {len(mpr_coords)} MPR points")
                self.parse_points(mpr_coords, self.mpr_point_array)

            try:
                length_coords = file['length points']
            except KeyError:
                logging.info(f"Found no length points")
            else:
                logging.info(f"Found {len(length_coords)} length points")
                self.parse_points(length_coords, self.length_point_array)

    def parse_points(self, points_from_json, point_array: PointArray):
        dcm_reader = DICOMReader(case_name=self.case_name,
                                 case_id=get_case_id(self.case_name),
                                 folder=self.filename.parents[1],
                                 is_new_case=False)

        np_array, file_list = dcm_reader[self.sequence_name]

        image_properties = SliceLocImageProperties(np_array=np_array,
                                                   z_coords=dcm_reader.get_z_coords(self.sequence_name),
                                                   file_list=file_list)

        for pt in points_from_json:
            parsed = Point.point_from_vtk_coords(pt, image_properties)
            point_array.add_point(parsed)

    def __repr__(self):
        return f"""
        Importing {self.filename} into database
        Timestamp  {self.timestamp}
        Time measured {self.time_measured}
        Length Points: {len(self.length_point_array)}
        MPR Points: {len(self.mpr_point_array)}
        """

    def commit(self):
        if self.time_measured and len(self.time_measured.strip()) > 0:
            timer = DummyTimer(self.time_measured.strip())
        else:
            timer = Timer()

        save_points(case_name=self.case_name,
                    sequence_name=self.sequence_name,
                    length_points=self.length_point_array,
                    mpr_points=self.mpr_point_array,
                    timer_data=timer,
                    timestamp=self.timestamp)


class DummyTimer(Timer):
    def __init__(self, gap_from_file):
        super().__init__()
        from datetime import datetime, timedelta

        clean_gap_string = gap_from_file.split(".")[0]

        t = datetime.strptime(clean_gap_string, "%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        self.measured_gap = delta

    def calculate_time_gap(self):
        return int(self.measured_gap.total_seconds())
