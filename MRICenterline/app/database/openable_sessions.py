import sqlite3
from MRICenterline import CFG


def get_all_sessions():
    con = sqlite3.connect(CFG.get_db())
    sessions = con.cursor().execute("""
                                    select session_id, lengths_id, cl_id, timestamp, case_name, name  
                                    from sessions 
                                    inner join case_list 
                                       on case_list.case_id = sessions.case_id 
                                    inner join sequences 
                                       on sequences.seq_id = sessions.seq_id
                                    """).fetchall()

    sessions_list, case_names, timestamps, seq_names, length, centerline = [], [], [], [], [], []
    for session_id, lengths_id, cl_id, timestamp, case_name, name in sessions:
        case_names.append(case_name)
        timestamps.append(timestamp)
        seq_names.append(name)
        sessions_list.append(session_id)

        if lengths_id:
            length.append(con.cursor().execute(
                f"select count(*) from 'length_coordinates' where lengths_id_id = {lengths_id}").fetchone()[0])
        else:
            length.append(0)

        if cl_id:
            centerline.append(con.cursor().execute(
                f"SELECT count(*) FROM 'centerline_coordinates' where cl_id = {cl_id}").fetchone()[0])
        else:
            centerline.append(0)

    con.close()

    return {"case name": case_names,
            "timestamps": timestamps,
            "sequence name": seq_names,
            'length points': length,
            'centerline points': centerline,
            'session_id': sessions_list}, len(sessions)


def get_latest_sessions():
    pass