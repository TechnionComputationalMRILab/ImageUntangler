#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save sequences to CSV
"""
import csv
import sqlite3
from MRICenterline import CFG


def sequence_report(save_to):
    columns = ['Case Name', 'Case Type', 'Sequence Name', 'Scan Orientation']

    con = sqlite3.connect(CFG.get_db())
    cases = con.cursor().execute("""
                                 select case_name, case_type, name, orientation 
                                 from case_list 
                                 inner join sequences 
                                 on case_list.case_id = sequences.case_id 
                                 where sequences.name != 'INVALID'
                                 """).fetchall()
    con.close()

    with open(save_to, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)

        writer.writeheader()

        for i in cases:
            i = list(i)
            i[3] = decode_orientation(i[3])
            d = dict(zip(columns, i))
            writer.writerow(d)

    return f"Sequence Report CSV file saved to {save_to}"


def decode_orientation(orientation_key):
    if orientation_key == "C":
        return "Coronal"
    elif orientation_key == "A":
        return "Axial"
    elif orientation_key == "S":
        return "Sagittal"
    else:
        return "Unknown"


if __name__ == '__main__':
    sequence_report("sequence.csv")
