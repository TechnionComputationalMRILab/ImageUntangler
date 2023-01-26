from typing import List, Tuple
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

DEFAULT_CASE_GROUPBY = (DICOMTag.PatientID, )
DEFAULT_SEQUENCE_GROUPBY = (DICOMTag.SeriesDescription, DICOMTag.SeriesNumber, DICOMTag.AcquisitionDate)


class SequenceType(Enum):
    DICOM = "DICOM"


class Sequence:
    __slots__ = (
        "filetype",
        "files",
        "metadata",
        "name"
    )

    @property
    def image_orientation(self):
        return ""

    def get_sitk_image(self):
        pass

    def get_numpy_array(self):
        pass

    def __repr__(self):
        return f"Sequence {self.name} " \
               f"| Type: {self.filetype} | File count: {len(self.files)} " \
               f"| {self.metadata}"


class Case:
    __slots__ = (
        "metadata",
        "files",
        "sequences",
        "name"
    )

    def __repr__(self):
        return f"Case {self.name} " \
               f"| File count: {len(self.files)} | Sequence count: {len(self.sequences)} " \
               f"| {self.metadata}"


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

    def scan_dicom(self):
        case_groupby = self._kwargs["sort_dicom_cases_by"] \
            if "sort_dicom_cases_by" in self._kwargs else DEFAULT_CASE_GROUPBY
        sequence_groupby = self._kwargs["sort_dicom_sequences_by"] \
            if "sort_dicom_sequences_by" in self._kwargs else DEFAULT_SEQUENCE_GROUPBY

        cases_found = self._read_dicom_cases(sort_by=case_groupby)
        self._read_dicom_case_metadata(cases_found)

        if self._verbose: print("Reading sequences")

        pbar = tqdm(enumerate(self.cases)) if self._pbar else enumerate(self.cases)
        for idx, case in pbar:
            if self._very_verbose: print((idx + 1, len(self.cases)))
            sequences_found = self._read_dicom_sequences(case, sequence_groupby)
            self._read_dicom_sequence_metadata(case, sequences_found)

    def _read_dicom_cases(self, sort_by: Tuple[DICOMTag]):
        files: List[Path] = [f for f in self.root_folder.rglob("*")]

        if self._verbose: print("Identifying DICOM cases")
        return self._group_by(files, sort_by, show_pbar=self._pbar, pbar_desc="Reading cases")

    def _read_dicom_case_metadata(self, cases_found):
        if self._verbose: print("Reading case metadata")

        pbar = tqdm(enumerate(cases_found.items())) if self._pbar else enumerate(cases_found.items())
        for idx, (case_sorter, files) in pbar:
            if self._very_verbose: print((idx + 1, len(cases_found)))
            c = Case()
            c.files = files
            c.name = str(case_sorter)

            c.metadata = {}
            for k, v in get_metadata_dict_from_itk(str(files[0]),
                                                   verbose=self._very_verbose).items():
                if k != DICOMTag.Unspecified:
                    if not k.name.startswith("Series"):
                        c.metadata[k] = v

            self.cases.append(c)

    @staticmethod
    def _group_by(files: list, groupby_keys: tuple, skip_none: bool = True,
                  show_pbar: bool = False, pbar_desc: str = "",
                  verbose: bool = False):
        found = {}
        pbar = tqdm(files) if show_pbar else files
        for f in pbar:
            if show_pbar: pbar.set_description(f"{pbar_desc}: {f}")
            if f not in found.keys():
                found[f] = [None] * len(groupby_keys)

            for k, v in get_metadata_dict_from_itk(f,
                                                   verbose=verbose).items():
                if k in groupby_keys:
                    found[f][groupby_keys.index(k)] = v

            found[f] = tuple(found[f])

        d = {}
        for f, group_values in found.items():
            if skip_none and all(group_values):
                if group_values not in d.keys():
                    d[group_values] = []
                d[group_values].append(f)

        return d

    def _read_dicom_sequences(self, case: Case, sequence_groupby: Tuple[DICOMTag]):
        case_path = case.files[0].parent

        seq_dict = self._group_by(case.files, sequence_groupby, verbose=self._very_verbose)
        return {key: [Path(case_path) / f for f in files] for key, files in seq_dict.items()}

    def _read_dicom_sequence_metadata(self, case: Case, sequences_found):
        case.sequences = []
        sequences_with_one_file = []
        for seq_key, files in sequences_found.items():
            if len(files) > 1:
                seq = Sequence()
                seq.name = str(seq_key)
                seq.filetype = SequenceType.DICOM
                seq.files = files
                seq.metadata = {}
                for k, v in get_metadata_dict_from_itk(str(files[0]),
                                                       verbose=self._very_verbose).items():
                    if k.name.startswith("Series"):
                        seq.metadata[k] = v

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
            for k, v in get_metadata_dict_from_itk(str(sequences_with_one_file[0]),
                                                   verbose=self._very_verbose).items():
                if k.name.startswith("Series"):
                    seq.metadata[k] = v

            case.sequences.append(seq)

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


def get_metadata_dict_from_itk(f, verbose: bool = False):
    import io
    from contextlib import redirect_stdout
    stdout = io.StringIO()

    out = {}
    try:
        with redirect_stdout(stdout):
            file_reader = sitk.ImageFileReader()
            file_reader.SetFileName(str(f))
            file_reader.ReadImageInformation()
        if verbose: print(stdout)
    except RuntimeError as runtime_error:
        if "Unable to determine ImageIO reader" in str(runtime_error):
            if verbose: print(f"sitk cannot read file {f}")
    except Exception as e:
        if verbose: print(f"{f} error: {e}")
    else:
        out = {DICOMTag.from_sitk_string(k): file_reader.GetMetaData(k) for k in file_reader.GetMetaDataKeys()}
    return out

if __name__ == "__main__":
    ROOT_FOLDER = r"C:\Users\ang.a\Database\Rambam MRE 082022 Full\1024089432272"

    db = Database(ROOT_FOLDER, pbar=True)
    db.generate_csv_report(r"C:\Users\ang.a\Desktop\out.csv")
