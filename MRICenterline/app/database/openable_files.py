import sqlite3
from MRICenterline import CFG

"""
Helper functions for building the tables shown in the custom load dialogs. This generates the
tables used by the "Open MRI images" button
"""


def get_openable_sequences():
    con = sqlite3.connect(CFG.get_db())
    cases = con.cursor().execute("""
                                 select case_name, case_type, name, orientation 
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

    columns = con.cursor().execute("""
                                   select name 
                                   from pragma_table_info('metadata')
                                   """).fetchall()

    cases = con.cursor().execute("""
                                 select * 
                                 from 'metadata' 
                                 inner join case_list 
                                 on case_list.case_id = metadata.case_id
                                 """).fetchall()
    con.close()

    columns = [i[0] for i in columns]
    columns.extend(['case_id', 'case_name', 'case_type'])

    out_dict = dict()
    for col_idx, col in enumerate(columns):
        temp_list = [dat[col_idx] for dat_idx, dat in enumerate(cases)]
        out_dict[col] = temp_list

    out_dict.pop('case_id')

    return out_dict, len(out_dict.keys()), len(cases)


if __name__ == "__main__":
    import os

    os.path.join(CFG.get_folder('raw_data'), "casename")
    zipped = list(zip(get_openable_sequences()[0]['case_name'], get_openable_sequences()[0]['sequences']))
    print(zipped)
