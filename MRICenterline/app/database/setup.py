case_list = '''
create table case_list (
case_id integer primary key autoincrement,
case_name text,
case_type text
)
'''

case_access_history = '''
create table case_access_history (
timestamp datetime,
seq_id integer,
case_id integer,
foreign key (case_id) references case_list(case_id) 
)
'''

metadata = '''
create table metadata (
StudyTime text, 
StudyDescription text, 
AcquisitionTime text, 
PatientName text, 
PatientID text, 
PatientAge text, 
PatientSex text, 
PatientBirthDate text, 
PatientPosition text, 
Manufacturer text, 
ManufacturerModelName text, 
ProtocolName text,
case_id integer,
foreign key (case_id) references case_list(case_id) 
)
'''

sequences = '''
create table sequences (
seq_id,
name text,
case_id integer,
foreign key (case_id) references case_list(case_id) 
)
'''

sequence_files = '''
create table sequence_files (
file_id integer primary key autoincrement, 
filename text, 
seq_id integer,
case_id integer,
foreign key (seq_id) references sequences(seq_id),
foreign key (case_id) references case_list(case_id) 
)
'''

slice_locations = '''
create table slice_locations (
slice_location real,
file_id integer,
foreign key (file_id) references sequence_files(file_id)
)
'''

sessions = """
create table sessions (
session_id integer primary key autoincrement,
timestamp datetime,
time_elapsed_seconds integer,
lengths_id integer,
cl_id integer,
seq_id integer,
case_id integer,
foreign key (lengths_id) references length_coordinates(lengths_id),
foreign key (cl_id) references centerline_coordinates(cl_id),
foreign key (seq_id) references sequences(seq_id),
foreign key (case_id) references case_list(case_id) 
)
"""

centerlines = """
create table centerline_coordinates (
pt_id integer primary key autoincrement,
cl_id integer,
x real,
y real,
z real 
)
"""

lengths = """
create table length_coordinates (
pt_id integer primary key autoincrement,
lengths_id integer,
x real,
y real,
z real 
)
"""

sql_strings = {
    'case_list': case_list,
    'case_access_history': case_access_history,
    'metadata': metadata,
    'sequences': sequences,
    'sequence_files': sequence_files,
    'slice_locations': slice_locations,
    'sessions': sessions,
    'centerlines': centerlines,
    'lengths': lengths
}


def db_init(metadata_path):
    import sqlite3

    con = sqlite3.connect(metadata_path)
    with con:
        for table_name, query in sql_strings.items():
            con.execute(query)
    con.close()
