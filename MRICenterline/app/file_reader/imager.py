import os
import sqlite3

from MRICenterline.app.file_reader.dicom.DICOMReader import DICOMReader
from MRICenterline.app.database.filetype import read_folder

from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


class Imager:
    def __init__(self, directory):
        self.directory = directory
        self.case_name = os.path.relpath(directory, CFG.get_folder('raw'))

        self.database_check()
        self.assign_reader()

    ##############################################
    #              public functions              #
    ##############################################

    def get_case_id(self) -> int:
        return self.reader.case_id

    def get_sequences(self) -> list:
        return self.reader.sequence_list

    def get_sequences_and_ids(self) -> tuple:
        return tuple(zip(range(1, len(self)+1), self.reader.sequence_list))

    def __len__(self) -> int:
        return len(self.reader)

    def get_files(self, seq):
        return self.reader.get_file_list(seq)

    ##############################################
    #             private functions              #
    ##############################################

    def database_check(self):
        """
        looks for the metadata.db
        checks if it has the case_list table
        and if the case being opened is in the database
        """

        con = sqlite3.connect(CFG.get_db())
        available_cases = [item[0] for item in con.cursor().execute("select case_name from case_list;").fetchall()]

        if self.case_name in available_cases:
            # skips the read_folder part, assigns self.file_type according to what the db says
            logging.debug(f"Found case {self.case_name} in database, reading file type from table")
            execute = con.cursor().execute(f"select * from case_list where case_name='{self.case_name}';").fetchone()

            self.new_case_flag = False
            self.case_id = execute[0]
            # self.case_name = execute[1]
            self.file_type = execute[2]

        else:
            # if missing, send it to the file readers
            self.initialize_folder()
            self.new_case_flag = True

        con.close()

    def assign_reader(self):
        if self.file_type.upper() == "DICOM":
            self.reader = DICOMReader(self.case_id, self.directory, self.new_case_flag)
        elif self.file_type.upper() == "NRRD":
            pass
        else:
            MSG.msg_box_warning("Either that format is not yet implemented or there are no MRI images there.")
            raise NotImplementedError

        logging.debug(f"Assigning reader as {self.file_type}")

    def initialize_folder(self):
        logging.debug("Checking folder type")
        self.file_type = read_folder(self.directory)
        logging.debug(f"Folder {self.directory} is type {self.file_type}")

        # add the folder to the case_list table
        con = sqlite3.connect(CFG.get_db())
        with con:
            con.execute('insert into case_list (case_name, case_type) values (?, ?)', (self.case_name, self.file_type,))
            self.case_id = con.execute('SELECT max(case_id) FROM case_list').fetchone()[0]
        con.close()
