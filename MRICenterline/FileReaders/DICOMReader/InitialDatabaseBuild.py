import os
from pathlib import Path
from glob import glob
import pydicom
import sqlite3

from MRICenterline.Config import CFG


def build(folder):
    case_name = os.path.relpath(folder, CFG.get_folder('raw'))
    # get case_id
    con = sqlite3.connect(CFG.get_db())
    cases = {i[1]: i[0] for i in con.cursor().execute("select * from 'case_list'").fetchall()}
    try:
        case_id = cases[case_name]
    except KeyError:
        raise KeyError("Case not found")
    else:
        build_sequence_tables(folder, case_id)
        build_metadata_table(folder, case_id)
        con.close()


def build_metadata_table(folder, case_id):
    """ creates the entry for the metadata of the database """
    db_file = CFG.get_db()
    con = sqlite3.connect(db_file)

    # get a random file from the database
    query_to_random_valid_file = f"""
                                 select filename
                                 from sequence_files
                                 inner join sequences
                                 on sequences.seq_id = sequence_files.seq_id
                                 where sequences.name != "INVALID"
                                 and sequences.case_id = {case_id}
                                 order by random()
                                 limit 1
                                 """

    random_file = con.cursor().execute(query_to_random_valid_file).fetchone()
    column_names = [item[0] for item in
                    con.cursor().execute("select name from pragma_table_info('metadata');").fetchall()]
    column_names.remove('case_id')  # remove 'case_id' from the list

    filename = os.path.join(folder, random_file[0])
    patient_data = pydicom.dcmread(filename)

    metadata_list = []
    for col in column_names:
        try:
            metadata_list.append(str(patient_data[col].value))
        except:
            metadata_list.append(None)
    metadata_list.append(case_id)

    print(column_names)
    print(metadata_list)

    with con:
        con.execute('insert into metadata values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', metadata_list)

    con.close()


def build_sequence_tables(folder, case_id):
    """
    Builds the sequences and sequence_files tables for the database
    """
    db_file = CFG.get_db()
    files_list = [Path(file) for file in glob(f'{folder}/*')]
    con = sqlite3.connect(db_file)

    ##########################
    # create sequence dictionary
    ##########################

    invalid_files = []
    seq_list = {}
    sorted_files = {}
    for filename in files_list:
        _file = os.path.basename(filename)

        try:
            dicom_info = pydicom.dcmread(filename)
            seq_name = dicom_info['SeriesDescription'].value
        except:
            invalid_files.append(_file)
        else:
            if seq_name:  # ignores blank sequence names
                if seq_name in seq_list:
                    sorted_files[seq_name][_file] = _file
                else:
                    sorted_files[seq_name] = {_file: _file}
                    seq_list[seq_name] = seq_name
            else:
                invalid_files.append(_file)

    seq_list = [seq_val[1] for seq_val in seq_list.items()]
    seq_list = set(seq_list)

    last_seq_id = 0
    for seq_id, seq_name in enumerate(seq_list):
        seq_files_list = [file_entry[1] for file_entry in sorted_files[seq_name].items()]

        with con:
            con.execute('insert into sequences (case_id, name, seq_id) values (?, ?, ?)',
                                               (case_id, seq_name, seq_id + 1))

            for file in seq_files_list:
                con.execute('insert into sequence_files (filename, seq_id, case_id) values (?, ?, ?)',
                                                        (file,   seq_id + 1, case_id))
        last_seq_id = seq_id + 2

    with con:  # insert files to be ignored
        con.execute('insert into sequences (case_id, name, seq_id) values (?, ?, ?)',
                                           (case_id, "INVALID", last_seq_id, ))
        for file in invalid_files:
            con.execute('insert into sequence_files (filename, seq_id, case_id) values (?, ?, ?)',
                                                    (file, last_seq_id, case_id))

    con.close()
