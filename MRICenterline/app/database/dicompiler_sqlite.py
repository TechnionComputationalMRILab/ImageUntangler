import sqlite3
from tqdm import tqdm
from pathlib import Path
from MRICenterline.external.dicompiler import Database, DICOMTag
from MRICenterline.app.database.setup import db_init

relevant_metadata = [
    DICOMTag.Manufacturer, DICOMTag.ManufacturerModelName,
    DICOMTag.StudyTime, DICOMTag.StudyDescription, DICOMTag.AcquisitionTime,
    DICOMTag.PatientName, DICOMTag.PatientID, DICOMTag.PatientSex, DICOMTag.PatientPosition,
    DICOMTag.ProtocolName
]


class SQLiteDatabase(Database):
    def generate_sqlite(self, sqlite_destination: str | Path):
        sqlite_destination = Path(sqlite_destination) if isinstance(sqlite_destination, str) else sqlite_destination
        if sqlite_destination.is_dir():
            sqlite_destination = sqlite_destination / "data.db"

        db_init(sqlite_destination)
        con = sqlite3.connect(sqlite_destination)

        case_name_tag = self._kwargs["sort_dicom_by"] if "sort_dicom_by" in self._kwargs else DICOMTag.PatientID
        values_string = "(" + len(relevant_metadata) * "?, " + "? )"

        with con:
            pbar = tqdm(enumerate(self.cases)) if self._pbar else enumerate(self.cases)
            for case_id, case in pbar:
                # insert case names
                # case_name = case.metadata[case_name_tag]
                case_name = str(case.files[0].parent.relative_to(self.root_folder))
                con.execute('insert into case_list (case_name, case_type) values (?, ?)',
                            (case_name, "DICOM",))

                # insert case metadata
                metadata_values = []
                for req_tag in relevant_metadata:
                    if req_tag in case.metadata.keys():
                        metadata_values.append(case.metadata[req_tag])
                    else:
                        metadata_values.append(None)

                con.execute(f'insert into metadata values {values_string}', (*metadata_values, case_id + 1))

                # insert sequences
                for seq_id, seq in enumerate(case.sequences):
                    seq_name = seq.metadata[DICOMTag.SeriesDescription] if DICOMTag.SeriesDescription in seq.metadata else "No series description"
                    seq_num = seq.metadata[DICOMTag.SeriesNumber] if DICOMTag.SeriesNumber in seq.metadata else 0

                    con.execute('insert into sequences (case_id, name, seq_id, orientation) values (?, ?, ?, ?)',
                                (case_id + 1, f"({seq_name}, {seq_num})", seq_id + 1, "X"))

                    if DICOMTag.Unspecified in seq.metadata:
                        pass
                    else:
                        for file in seq.files:
                            con.execute('insert into sequence_files (filename, seq_id, case_id) values (?, ?, ?)',
                                        (file.name, seq_id + 1, case_id + 1))

        con.close()

    def append_to_sqlite(self, sqlite_file: str | Path):
        pass


if __name__ == "__main__":
    sqlite_db = SQLiteDatabase(r"C:\Users\ang.a\Database\Rambam MRE 082022 Full", verbose=True, pbar=True)
    sqlite_db.generate_sqlite(r"C:\Users\ang.a\Database\Rambam MRE 082022 Full\metadata.db")
