import sqlite3
import pytz
from datetime import datetime, timezone

from MRICenterline.app.database import name_id
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.points.timer import Timer

from MRICenterline import CFG, CONST, MSG

import logging
logging.getLogger(__name__)


def save_points(case_name: str,
                sequence_name: str,
                length_points: PointArray,
                mpr_points: PointArray,
                timer_data: Timer,
                timestamp: datetime or None = None):

    case_id = name_id.get_case_id(case_name)
    seq_id = name_id.get_sequence_id(sequence_name, case_id)

    if timestamp:
        # convert timestamp to UTC and then to string
        timestamp_string = timestamp.astimezone(pytz.utc).strftime(CONST.TIMESTAMP_FORMAT)
    else:
        # use timezone now
        timestamp_string = datetime.utcnow().strftime(CONST.TIMESTAMP_FORMAT)
    time_gap = timer_data.calculate_time_gap()

    con = sqlite3.connect(CFG.get_db())

    logging.debug(f"Inserting {len(length_points)} length points")
    if len(length_points):
        lengths_id = con.cursor().execute("""
                                          select count(*) 
                                          from (
                                              select distinct lengths_id 
                                              from 'length_coordinates'
                                              )""").fetchone()[0] + 1
        for pt in length_points:
            length_insert_query = """insert into 'length_coordinates'
                                     (lengths_id, x, y, z)
                                     values
                                     (?, ?, ?, ?)
                                  """
            with con:
                if CFG.get_testing_status("use-slice-location"):
                    con.execute(length_insert_query, (lengths_id, *pt.image_coordinates))
                else:
                    con.execute(length_insert_query, (lengths_id, *pt.physical_coords))
    else:
        lengths_id = None

    logging.debug(f"Inserting {len(mpr_points)} MPR points")
    if len(mpr_points):
        cl_id = con.cursor().execute("""
                                     select count(*) 
                                     from (
                                         select distinct cl_id
                                         from 'centerline_coordinates'
                                         )""").fetchone()[0] + 1
        for pt in mpr_points:
            cl_insert_query = """insert into centerline_coordinates
                                 (cl_id, x, y, z)
                                 values
                                 (?, ?, ?, ?)
                            """
            with con:
                if CFG.get_testing_status("use-slice-location"):
                    con.execute(cl_insert_query, (cl_id, *pt.image_coordinates))
                else:
                    con.execute(cl_insert_query, (cl_id, *[float(i) for i in pt.itk_index_coords]))
    else:
        cl_id = None

    session_data = {
        'timestamp': timestamp_string,
        'time_elapsed_seconds': time_gap,
        'lengths_id': lengths_id,
        'cl_id': cl_id,
        'seq_id': seq_id,
        'case_id': case_id
    }

    logging.debug(f"Inserting session data")
    with con:
        con.execute("""insert into sessions 
                       (timestamp, time_elapsed_seconds, lengths_id, cl_id, seq_id, case_id) 
                       values
                       (:timestamp, :time_elapsed_seconds, :lengths_id, :cl_id, :seq_id, :case_id)
                    """,
                    session_data)

    session_id = con.cursor().execute("select count(*) from 'sessions'").fetchone()[0]
    con.close()

    session_saved_message = f"Saved session with id [{session_id}] successfully."
    logging.info(session_saved_message)
    MSG.msg_box_info(session_saved_message)

    return session_id
