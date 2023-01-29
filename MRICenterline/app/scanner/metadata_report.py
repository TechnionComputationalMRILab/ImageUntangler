#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exports the metadata of a database to a CSV file
"""
import sqlite3
from MRICenterline import CFG
import csv


def metadata_report(save_to):

    con = sqlite3.connect(CFG.get_db())

    columns = con.cursor().execute("""
                                   select name 
                                   from pragma_table_info('metadata')
                                   """).fetchall()

    cases = con.cursor().execute("""
                                 select StudyTime, 
                                        StudyDescription, 
                                        AcquisitionDate, 
                                        PatientName, 
                                        PatientID, 
                                        PatientSex, 
                                        PatientPosition, 
                                        Manufacturer, 
                                        ManufacturerModelName, 
                                        ProtocolName, 
                                        case_name, 
                                        case_type
                                 from 'metadata' 
                                 inner join case_list 
                                 on case_list.case_id = metadata.case_id
                                 """).fetchall()
    con.close()

    columns = [i[0] for i in columns]
    columns.remove("case_id")  # case_id is only used internally by the program
    columns.extend(['case_name', 'case_type'])

    with open(save_to, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)

        writer.writeheader()

        for i in cases:
            d = dict(zip(columns, i))
            writer.writerow(d)

    return f"Metadata CSV file saved to {save_to}"


if __name__ == '__main__':
    metadata_report("metadata.csv")
