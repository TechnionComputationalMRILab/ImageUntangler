import sqlite3


def check_db_version(db_file_path):
    conn = sqlite3.connect(db_file_path)

    if conn.execute("select * from sqlite_master WHERE type='table' AND name='internal_metadata'").fetchone():
        return conn.execute("select software_version from 'internal_metadata'").fetchone()
    else:
        return "INV"
