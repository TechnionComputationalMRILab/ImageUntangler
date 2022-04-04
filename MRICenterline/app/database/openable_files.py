import sqlite3
from MRICenterline import CFG


def get_openable_sequences():
    con = sqlite3.connect(CFG.get_db())
    cases = con.cursor().execute("""
                                 select case_name, case_type, name 
                                 from case_list 
                                 inner join sequences 
                                 on case_list.case_id = sequences.case_id 
                                 where sequences.name != 'INVALID'
                                 """).fetchall()
    con.close()

    names, file_types, seq_names = [], [], []
    for name, file_type, sequence_name in cases:
        names.append(name)
        file_types.append(file_type)
        seq_names.append(sequence_name)

    return {"case_name": names,
            "case_type": file_types,
            "sequences": seq_names}, len(cases)


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
