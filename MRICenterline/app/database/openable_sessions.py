import sqlite3

from MRICenterline.app.database import name_id
from MRICenterline import CFG


def get_all_sessions():
    con = sqlite3.connect(CFG.get_db())
    sessions = con.cursor().execute("select * from 'sessions'").fetchall()
    session_table_headers = [i[1] for i in con.cursor().execute("select * from pragma_table_info('sessions');").fetchall()]

    dat = {h: list() for h in session_table_headers}
    for s in sessions:
        conv = list(s)
        conv[5] = name_id.get_sequence_name(s[5], s[6])
        conv[6] = name_id.get_case_name(s[6])
        for (_, li), i in zip(dat.items(), conv):
            li.append(i)

    con.close()

    dat.pop('lengths_id')
    dat.pop('cl_id')
    return dat, len(sessions)


def get_latest_sessions():
    # select * from 'sessions' group by case_id order by timestamp desc
    pass


if __name__ == "__main__":
    print(get_all_sessions())
