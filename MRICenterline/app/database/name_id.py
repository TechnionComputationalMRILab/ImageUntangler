import sqlite3
from MRICenterline import CFG


def get_case_id(case_name: str):
    con = sqlite3.connect(CFG.get_db())
    case_id = con.cursor().execute(f"select case_id from case_list where case_name='{case_name}';").fetchone()[0]
    con.close()
    return case_id


def get_case_name(case_id: int):
    con = sqlite3.connect(CFG.get_db())
    case_name = con.cursor().execute(f"select case_name from case_list where case_id={case_id};").fetchone()[0]
    con.close()
    return case_name


def get_sequence_name(seq_id: int, case):
    if type(case) is str:
        case = get_case_id(case)
    else:
        case = int(case)

    con = sqlite3.connect(CFG.get_db())
    sequence_name = con.cursor().execute(f"SELECT name FROM 'sequences' where seq_id={seq_id} and case_id='{case}'").fetchone()[0]
    con.close()

    return sequence_name


def get_sequence_id(seq_name: str, case):
    if type(case) is str:
        case = get_case_id(case)
    else:
        case = int(case)

    con = sqlite3.connect(CFG.get_db())
    sequence_id = con.cursor().execute(f"SELECT seq_id FROM 'sequences' where name='{seq_name}' and case_id='{case}'").fetchone()[0]
    con.close()

    return sequence_id


def from_session_id(session_id: int):
    con = sqlite3.connect(CFG.get_db())
    seq_id, case_id, lengths_id, cl_id = con.cursor().execute(f"select seq_id, case_id, lengths_id, cl_id from 'sessions' where session_id={session_id}").fetchone()
    con.close()

    return seq_id, case_id, lengths_id, cl_id
