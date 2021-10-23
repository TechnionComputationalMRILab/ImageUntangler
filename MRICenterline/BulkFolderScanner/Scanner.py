import os
import json
from glob import glob
from pydicom import dcmread

from MRICenterline.FileReaders.DICOMReader import DICOMReader


def get_directories(folder):
    return glob(f"{folder}/*/")


def generate_seq_dict(folder):
    _dicomreader = DICOMReader.test_folder(folder, run_clean=True)
    if _dicomreader is type(DICOMReader):
        if _dicomreader.check_seqfile_exists():
            _dicomreader.generate_seq_dict()


def generate_report(folder):
    required_fields = ["PatientName", "PatientID", "Manufacturer", "ManufacturerModelName", "ProtocolName", "StudyDate", "StudyTime"]
    _dicomreader = DICOMReader.test_folder(folder)

    if type(_dicomreader) is DICOMReader:
        get_first_valid_file = list(_dicomreader.sequence_dict.values())[-1][-1]
        patient_data = dcmread(os.path.join(folder, get_first_valid_file))

        filled_out_dict = {}
        filled_out_dict['Sequences'] = _dicomreader.get_sequence_list()
        for item in required_fields:
            filled_out_dict[item] = patient_data[item].value

        return filled_out_dict
    else:
        return None


def generate_directory_report(folder, get_only_latest, also_show_centerline):
    try:
        os.remove(os.path.join(folder, 'directory.csv'))
    except Exception:
        pass

    # go through all the data directories
    _data_directories = [file.replace('\\', '/') for file in glob(f"{folder}/*/data/")]
    _to_csv = []

    for di in _data_directories:
        _centerline_annotation_data = set(
            [file.replace('\\', '/') for file in glob(f"{di}/*.centerline.annotation.json")])

        if _centerline_annotation_data:
            _annotation_data = set(
                [file.replace('\\', '/') for file in glob(f"{di}/*.annotation.json")]) - _centerline_annotation_data
        else:
            _annotation_data = set([file.replace('\\', '/') for file in glob(f"{di}/*.annotation.json")])

        if _annotation_data:
            _dict = {}
            if get_only_latest:
                _latest_annotation = max(_annotation_data, key=os.path.getctime)

                with open(_latest_annotation, 'r') as annotation_file:
                    _file = json.load(annotation_file)
                    _dict["case number"] = [int(s) for s in di.split('/') if s.isdigit()][0]
                    _dict["sequence name"] = _file['SeriesDescription']
                    _dict['date'] = _file['annotation timestamp'][:10]
                    _dict['# MPR points'] = -999
                    _dict['# len points'] = -999
                    _dict['Time measurement'] = _file['Time measurement']
                    _dict['length'] = _file['measured length']
                    _dict['path'] = di
                    _dict['filename'] = os.path.basename(_latest_annotation)
                    _to_csv.append(_dict)

                if also_show_centerline and _centerline_annotation_data:
                    _latest_centerline_annotation = max(_centerline_annotation_data, key=os.path.getctime)

                    with open(_latest_centerline_annotation, 'r') as annotation_file:
                        _file = json.load(annotation_file)
                        _dict["case number"] = str([int(s) for s in di.split('/') if s.isdigit()][0]) + "-CL"
                        _dict["sequence name"] = _file['SeriesDescription']
                        _dict['date'] = _file['annotation timestamp'][:10]
                        _dict['# MPR points'] = -999
                        _dict['# len points'] = -999
                        _dict['Time measurement'] = _file['Time measurement']
                        _dict['length'] = _file['measured length']
                        _dict['path'] = di
                        _dict['filename'] = os.path.basename(_latest_centerline_annotation)
                        _to_csv.append(_dict)

    return _to_csv


def generate_time_report(folder):
    _data_directories = [file.replace('\\', '/') for file in glob(f"{folder}/*/data/")]
    _to_csv = []

    for di in _data_directories:
        _centerline_annotation_data = [file.replace('\\', '/') for file in glob(f"{di}/*.centerline.annotation.json")]
        if not _centerline_annotation_data:
            continue

        _annotation_data = list(set([file.replace('\\', '/') for file in glob(f"{di}/*.annotation.json")]) - set(
            _centerline_annotation_data))

        # get the latest dated annotation and centerline.annotation file
        _latest_annotation = max(_annotation_data, key=os.path.getctime)
        _latest_centerline_annotation = max(_centerline_annotation_data, key=os.path.getctime)

        # get the time measurements
        _dict = {}
        with open(_latest_annotation, 'r') as annotation_file, \
                open(_latest_centerline_annotation, 'r') as centerline_file:
            _dict['Annotation time measurement'] = json.load(annotation_file)['Time measurement']
            _dict['Centerline Annotation time measurement'] = json.load(centerline_file)['Time measurement']

        _dict['Case Number'] = [int(s) for s in di.split('/') if s.isdigit()][0]
        _dict['Path'] = di
        _to_csv.append(_dict)

    return _to_csv
