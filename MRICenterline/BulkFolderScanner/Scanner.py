from glob import glob
from MRICenterline.FileReaders.DICOMReader import DICOMReader
from pydicom import dcmread


def get_directories(folder):
    return glob(f"{folder}/*/")


def generate_seq_dict(folder):
    _dicomreader = DICOMReader.test_folder(folder)
    if _dicomreader is type(DICOMReader):
        if _dicomreader.check_seqfile_exists():
            _dicomreader.generate_seq_dict()


def generate_report(folder):
    required_fields = ["PatientName", "PatientID", "Manufacturer", "ManufacturerModelName", "ProtocolName", "StudyDate", "StudyTime"]
    _dicomreader = DICOMReader.test_folder(folder, run_clean=True)

    if type(_dicomreader) is DICOMReader:
        get_first_valid_file = list(_dicomreader.sequence_dict.values())[-1][-1]
        patient_data = dcmread(get_first_valid_file)

        filled_out_dict = {}
        filled_out_dict['Sequences'] = _dicomreader.get_sequence_list()
        for item in required_fields:
            filled_out_dict[item] = patient_data[item].value

        return filled_out_dict
    else:
        return None




