import sqlite3
import pandas as pd
from copy import deepcopy
from MRICenterline import CFG
from MRICenterline.app.database import name_id
from MRICenterline.app.database.calculate import calculate_total_length, get_number_of_cl_points


def time_report(save_as):
    session_table_headers = ["Timestamp", "Time Elapsed (seconds)", "Total Length Measured (mm)",
                             "Number of CL points", "Sequence Name", "Case Name"]

    con = sqlite3.connect(CFG.get_db())
    sessions = con.cursor().execute("""
                                    select timestamp, 
                                           time_elapsed_seconds, 
                                           lengths_id, 
                                           cl_id, 
                                           seq_id, 
                                           case_id 
                                    from 'sessions'
                                    """).fetchall()

    con.close()

    data = []
    for i in sessions:
        j = deepcopy(list(i))
        j[4] = name_id.get_sequence_name(i[4], i[5])
        j[5] = name_id.get_case_name(i[5])

        # i[3] == None : no centerlines were made
        # i[1] == 0 : timer not run
        # if i[3] and i[1]:
        j[2] = calculate_total_length(case_id=i[5], seq_id=i[4], lengths_id=i[2])
        j[3] = get_number_of_cl_points(i[3])

        data.append(dict(zip(session_table_headers, j)))

    df = pd.DataFrame(data)
    df.to_csv(save_as)
    return f"Time report saved to {save_as}"
