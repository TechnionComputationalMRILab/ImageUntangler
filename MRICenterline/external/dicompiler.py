from typing import List
from pathlib import Path
import SimpleITK as sitk
from enum import Enum
from tqdm import tqdm


class DICOMTag(Enum):
    Unspecified = 0xFFFF, 0xFFFF

    SeriesDescription = 0x0008, 0x103e
    SeriesInstanceUID = 0x0020, 0x000E
    SeriesNumber = 0x0020, 0x0011
    StudyInstanceUID = 0x0020, 0x000d

    PatientID = 0x0010, 0x0020
    FileSetID = 0x0004, 0x1130
    StudyTime = 0x0008, 0x0030
    StudyDescription = 0x0008, 0x1030
    AcquisitionDate = 0x0008, 0x0022
    AcquisitionTime = 0x0008, 0x0032
    PatientName = 0x0010, 0x0010
    PatientAge = 0x0010, 0x1010
    PatientSex = 0x0010, 0x0040
    PatientPosition = 0x0018, 0x5100
    Manufacturer = 0x0008, 0x0070
    ManufacturerModelName = 0x0008, 0x1090
    ProtocolName = 0x0018, 0x1030

    @staticmethod
    def from_sitk_string(sitk_string: str):
        tag1, tag2 = sitk_string.split("|")
        try:
            tag = DICOMTag((int(tag1, 16), int(tag2, 16)))
        except ValueError:
            tag = DICOMTag.Unspecified
        return tag


class SequenceType(Enum):
    DICOM = "DICOM"


class Sequence:
    __slots__ = (
        "filetype",
        "files",
        "metadata"
    )

    @property
    def image_orientation(self):
        return ""

    def get_sitk_image(self):
        pass

    def get_numpy_array(self):
        pass

    def __repr__(self):
        return f"{self.filetype} with {len(self.files)} | {self.metadata}"


class Case:
    __slots__ = (
        "metadata",
        "files",
        "sequences"
    )

    def __repr__(self):
        return f"Case with {len(self.files)} files, {len(self.sequences)} sequences | {self.metadata}"


class Database:
    __slots__ = (
        "root_folder",
        "cases",
        "_kwargs",
        "_verbose",
        "_very_verbose",
        "_pbar"
    )

    def __init__(self, root_folder: str | Path, **kwargs):
        self.root_folder = Path(root_folder) if isinstance(root_folder, str) else root_folder
        assert self.root_folder.is_dir(), "Root folder provided is not a directory"

        self._kwargs = kwargs
        self._verbose = self._kwargs["verbose"] if "verbose" in self._kwargs else False
        self._very_verbose = self._kwargs["vv"] if "v" in self._kwargs else False
        self._pbar = self._kwargs["pbar"] if "pbar" in self._kwargs else False

        self.cases: List[Case] = []

        skip_initial_scan = self._kwargs["skip_initial_scan"] if "skip_initial_scan" in self._kwargs else False

        if not skip_initial_scan:
            self.scan_dicom()

    def _read_dicom_cases(self, sort_by: DICOMTag):
        files: List[Path] = [f for f in self.root_folder.rglob("*")]

        if self._verbose: print("Identifying DICOM cases")

        cases_found = {}
        pbar = tqdm(files) if self._pbar else files
        for i, f in enumerate(pbar):
            if self._very_verbose: print((i + 1, len(files)))
            if f.is_dir():
                continue
            else:
                for k, v in self.get_metadata_dict_from_itk(str(f), verbose=self._verbose).items():
                    if DICOMTag.from_sitk_string(k) == sort_by:
                        if v not in cases_found:
                            cases_found[v] = []
                        cases_found[v].append(f)

        return cases_found

    def _read_dicom_case_metadata(self, cases_found):
        if self._verbose: print("Reading case metadata")

        pbar = tqdm(enumerate(cases_found.items())) if self._pbar else enumerate(cases_found.items())
        for idx, (case_sorter, files) in pbar:
            if self._very_verbose: print((idx + 1, len(cases_found)))
            c = Case()
            c.files = files

            c.metadata = {}
            for k, v in self.get_metadata_dict_from_itk(str(files[0])).items():
                tag = DICOMTag.from_sitk_string(k)
                if tag != DICOMTag.Unspecified:
                    if not tag.name.startswith("Series"):
                        c.metadata[tag] = v



            self.cases.append(c)

    def _read_dicom_sequences(self, case: Case):
        case.sequences = []
        sequences_found = {}
        case_path = case.files[0].parent

        for file in case.files:
            fn = file.name
            if fn not in sequences_found.keys():
                sequences_found[fn] = [None] * 4
                # study_uid, series_uid, series_desc, series_num

            for k, v in self.get_metadata_dict_from_itk(str(file)).items():
                match DICOMTag.from_sitk_string(k):
                    case DICOMTag.StudyInstanceUID:
                        sequences_found[fn][0] = v
                    case DICOMTag.SeriesInstanceUID:
                        sequences_found[fn][1] = v
                    case DICOMTag.SeriesDescription:
                        sequences_found[fn][2] = v
                    case DICOMTag.SeriesNumber:
                        sequences_found[fn][3] = v

        seq_dict = {}
        for f, (study_uid, series_uid, series_desc, series_num) in sequences_found.items():
            if series_num and series_desc:  # skip the files where these are None
                key = int(series_num), series_desc
                if key not in seq_dict.keys():
                    seq_dict[key] = []
                seq_dict[key].append(f)

        out_dict = {}
        for key, files in seq_dict.items():
            out_dict[key] = [Path(case_path) / f for f in files]

        return out_dict

    def _read_dicom_sequence_metadata(self, case: Case, sequences_found):
        sequences_with_one_file = []
        for _, files in sequences_found.items():
            if len(files) > 1:
                seq = Sequence()
                seq.filetype = SequenceType.DICOM
                seq.files = files
                seq.metadata = {}
                for k, v in self.get_metadata_dict_from_itk(str(files[0])).items():
                    tag = DICOMTag.from_sitk_string(k)
                    if tag.name.startswith("Series"):
                        seq.metadata[tag] = v

                case.sequences.append(seq)
            else:
                sequences_with_one_file.append(files)

        if len(sequences_with_one_file):
            if self._verbose:
                print(f"Single-file sequences found with {len(sequences_with_one_file)} files")
            seq = Sequence()
            seq.filetype = SequenceType.DICOM

            seq.files = sequences_with_one_file

            seq.metadata = {DICOMTag.Unspecified: "Single-file sequence"}
            for k, v in self.get_metadata_dict_from_itk(str(sequences_with_one_file[0])).items():
                tag = DICOMTag.from_sitk_string(k)
                if tag.name.startswith("Series"):
                    seq.metadata[tag] = v

            case.sequences.append(seq)

    @staticmethod
    def get_metadata_dict_from_itk(f, verbose: bool = False):
        out = {}
        try:
            file_reader = sitk.ImageFileReader()
            file_reader.SetFileName(str(f))
            file_reader.ReadImageInformation()
        except RuntimeError as runtime_error:
            if "Unable to determine ImageIO reader" in str(runtime_error):
                if verbose:
                    print(f"sitk cannot read file {f}")
        except Exception as e:
            if verbose:
                print(f"{f} error: {e}")
        else:
            out = {k: file_reader.GetMetaData(k) for k in file_reader.GetMetaDataKeys()}
        return out

    def generate_csv_report(self, file_destination: str | Path):
        import csv

        with open(file_destination, 'w', newline='') as csv_file:
            # populate field names
            field_names = ["RelativePath", "NumberOfSequences",
                           "(SeriesDescription, SeriesNumber, NumberOfFiles)"] \
                          + [k.name for k in self.cases[0].metadata.keys()]

            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

            for c in self.cases:
                clean_dict = {
                    "RelativePath": set([str(f.parent.relative_to(self.root_folder)) for f in c.files]),
                    "NumberOfSequences": len(c.sequences)
                }

                # metadata
                clean_dict |= {k.name: v for k, v in c.metadata.items()}

                # sequence data
                clean_dict |= {
                    "(SeriesDescription, SeriesNumber, NumberOfFiles)": [(
                        s.metadata[DICOMTag.SeriesDescription] if DICOMTag.SeriesDescription in s.metadata else "",
                        s.metadata[DICOMTag.SeriesNumber] if DICOMTag.SeriesNumber in s.metadata else "",
                        len(s.files)) for s in c.sequences]
                }

                writer.writerow(clean_dict)

    def scan_dicom(self):
        cases_found = self._read_dicom_cases(
            sort_by=self._kwargs["sort_dicom_by"] if "sort_dicom_by" in self._kwargs else DICOMTag.PatientID
        )

        self._read_dicom_case_metadata(cases_found)

        if self._verbose: print("Reading sequences")

        pbar = tqdm(enumerate(self.cases)) if self._pbar else enumerate(self.cases)
        for idx, case in pbar:
            if self._very_verbose: print((idx + 1, len(self.cases)))
            sequences_found = self._read_dicom_sequences(case)
            self._read_dicom_sequence_metadata(case, sequences_found)


if __name__ == "__main__":
    ROOT_FOLDER = r"C:\Users\ang.a\Database\HodgkinsRambam\1"

    db = Database(ROOT_FOLDER, pbar=True)
    db.generate_csv_report(r"C:\Users\ang.a\Desktop\out.csv")
