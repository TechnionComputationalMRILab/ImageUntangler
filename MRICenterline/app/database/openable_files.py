import sqlite3
from MRICenterline import CFG

"""
Helper functions for building the tables shown in the custom load dialogs. This generates the
tables used by the "Open MRI images" button
"""


def get_openable_sequences():
    con = sqlite3.connect(CFG.get_db())
    cases = con.cursor().execute("""
                                 select case_list.case_id, case_name, name, orientation 
                                 from case_list 
                                 inner join sequences 
                                 on case_list.case_id = sequences.case_id 
                                 where sequences.name != 'INVALID'
                                 """).fetchall()
    con.close()

    names, file_types, seq_names, orientation_list = [], [], [], []
    for name, file_type, sequence_name, orientation in cases:
        names.append(name)
        file_types.append(file_type)
        seq_names.append(sequence_name)
        orientation_list.append(orientation)

    return {"case_name": names,
            "case_type": file_types,
            "sequences": seq_names,
            "orientation": orientation_list}, len(cases)


def get_openable_cases():
    con = sqlite3.connect(CFG.get_db())
    con.row_factory = sqlite3.Row

    cases = con.cursor().execute("""
                                select distinct 
                                    case_list.case_id as "Case ID", 
                                    case_list.case_name as "Case Name", 
                                    metadata.Manufacturer, 
                                    metadata.AcquisitionDate
                                from 'metadata'
                                inner join case_list
                                    on case_list.case_id = metadata.case_id
                                 """).fetchall()
    con.close()

    query_out = [dict(r) for r in cases]
    out = {}
    for k in query_out[0].keys():
        out[k] = []

    for i in query_out:
        for k, v in i.items():
            out[k].append(v)

    return out, len(query_out[0].keys()), len(query_out)


if __name__ == "__main__":
    import os

    os.path.join(CFG.get_folder('raw_data'), "casename")
    zipped = list(zip(get_openable_sequences()[0]['case_name'], get_openable_sequences()[0]['sequences']))
    print(zipped)
