#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Used to upgrade from pre v.4.5.0 databases
"""
import sqlite3

import setup, check_db_version
from MRICenterline import CFG

new_table_strings = {
    'cl_lengths': setup.cl_lengths,
    "internal_metadata": setup.internal_metadata
}

new_table_names = ["cl_lengths_coordinates", "internal_metadata"]


def update_table(table_name, new_create_command, conn):
    columns = [i[1] for i in conn.execute(f"select * from pragma_table_info('{table_name}')").fetchall()]
    column_string = ",".join([f'"{i}"' for i in columns])

    create_copy = f"""
                  create temporary table temp_{table_name} as
                  select * from {table_name}
                  """
    with conn:
        conn.execute(create_copy)

        # drop the original table
        conn.execute(f"drop table {table_name}")

        conn.execute(new_create_command)
        conn.execute(f"insert into {table_name} ({column_string}) select {column_string} from temp_{table_name}")


def update_database(conn):
    from datetime import datetime
    from MRICenterline import CONST

    db_build_date = datetime.utcnow().strftime(CONST.TIMESTAMP_FORMAT)

    with conn:

        for t in new_table_names:
            conn.execute(f"drop table if exists {t}")

        for table_name, query in new_table_strings.items():
            conn.execute(query)

        update_table('sessions', setup.sessions, conn)

        conn.execute('insert into internal_metadata (software_version, software_build_date, '
                     '                                   db_build_date, is_upgraded) '
                     '                              values (?, ?, ?, ?)',
                     (CONST.VER_NUMBER, CONST.BUILD_DATE, db_build_date, 1))

    return True


if __name__ == "__main__":
    db_file = CFG.get_db()
    con = sqlite3.connect(db_file)

    update_database(con)
    # update_database(con)
    con.close()
