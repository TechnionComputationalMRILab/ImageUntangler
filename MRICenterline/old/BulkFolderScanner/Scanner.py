import os
import json
from glob import glob
from pydicom import dcmread
from pathlib import Path

from MRICenterline.FileReaders.DICOMReader import DICOMReader

import logging
logging.getLogger(__name__)


def get_directories(folder):
    _list = [Path(i) for i in glob(f"{folder}/**/", recursive=True)]

    for i in _list:
        if i.stem == 'data':
            _list.remove(i)

    # _list.remove(folder)
    return _list


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
            try:
                filled_out_dict[item] = patient_data[item].value
            except:
                filled_out_dict[item] = " "

        return filled_out_dict
    else:
        return None


def generate_directory_report(folder, get_only_latest, also_show_centerline):
    try:
        os.remove(os.path.join(folder, 'directory.csv'))
    except Exception:
        logging.debug("No directory file to delete!")

    # go through all the data directories
    _data_directories = [Path(file) for file in glob(f"{folder}/*/data/")]
    _to_csv = []

    for di in _data_directories:
        logging.debug(f"Scanning for annotations in {di}")
        _centerline_annotation_data = set([Path(file) for file in glob(f"{di}/*.centerline.annotation.json")])

        if _centerline_annotation_data:
            _annotation_data = set([Path(file) for file in glob(f"{di}/*.annotation.json")]) - _centerline_annotation_data
        else:
            _annotation_data = set([Path(file) for file in glob(f"{di}/*.annotation.json")])

        if _annotation_data:
            _dict = {}
            if get_only_latest:
                _latest_annotation = max(_annotation_data, key=os.path.getctime)
                logging.debug(f'Adding {_latest_annotation} to directory')

                with open(_latest_annotation, 'r') as annotation_file:
                    _file = json.load(annotation_file)
                    _dict["case number"] = [int(s) for s in str(Path(di)).split('\\') if s.isdigit()][0]
                    _dict["sequence name"] = _file['SeriesDescription']
                    _dict['date'] = _file['annotation timestamp'][:10]
                    _dict['# MPR points'] = -999
                    _dict['# len points'] = -999
                    _dict['Time measurement'] = _file['Time measurement'] if 'Time measurement' in _file.keys() else -999
                    _dict['length'] = _file['measured length'] if 'measured length' in _file.keys() else -999
                    _dict['path'] = os.path.dirname(di)
                    _dict['filename'] = os.path.basename(_latest_annotation)

                    if not _centerline_annotation_data:
                        logging.debug(f'No CL data found for {di}')
                        _dict['has CL'] = "CL not available"
                    else:
                        _latest_centerline_annotation = max(_centerline_annotation_data, key=os.path.getctime)
                        if os.path.getctime(_latest_centerline_annotation) > os.path.getctime(_latest_annotation):
                            logging.debug(f'Adding CL data {_latest_centerline_annotation}')
                            _dict['has CL'] = "CL available"
                        else:
                            _dict['has CL'] = "CL not available"
                            logging.debug("No compatible CL data found")

                    _to_csv.append(_dict)

                if also_show_centerline and _centerline_annotation_data:
                    _latest_centerline_annotation = max(_centerline_annotation_data, key=os.path.getctime)

                    with open(_latest_centerline_annotation, 'r') as annotation_file:
                        _file = json.load(annotation_file)
                        _dict["case number"] = str([int(s) for s in str(Path(di)).split('\\') if s.isdigit()][0]) + "-CL"
                        _dict["sequence name"] = _file['SeriesDescription']
                        _dict['date'] = _file['annotation timestamp'][:10]
                        _dict['# MPR points'] = -999
                        _dict['# len points'] = -999
                        _dict['Time measurement'] = _file['Time measurement'] if 'Time measurement' in _file.keys() else -999
                        # _dict['length'] = _file['length'] if 'measured length' in _file.keys() else -999
                        _dict['path'] = os.path.dirname(di)
                        _dict['filename'] = os.path.basename(_latest_centerline_annotation)
                        _to_csv.append(_dict)
        else:
            logging.debug(f"No annotations found in {di}")

    return _to_csv


def generate_time_report(folder):
    _data_directories = [Path(file) for file in glob(f"{folder}/*/data/")]
    _to_csv = []

    for di in _data_directories:
        logging.debug(f"Scanning {di}")

        _centerline_annotation_data = [Path(file) for file in glob(f"{di}/*.centerline.annotation.json")]
        if not _centerline_annotation_data:
            logging.debug(f"No CL data found for {di}. Continuing...")
            continue

        _annotation_data = list(set([Path(file) for file in glob(f"{di}/*.annotation.json")]) - set(
            _centerline_annotation_data))

        # get the latest dated annotation and centerline.annotation file
        _latest_annotation = max(_annotation_data, key=os.path.getmtime)
        _latest_centerline_annotation = max(_centerline_annotation_data, key=os.path.getmtime)

        if os.path.getmtime(_latest_centerline_annotation) > os.path.getmtime(_latest_annotation):
            logging.debug("Matching annotation/CL file found")
            # get the time measurements
            _dict = {}
            with open(_latest_annotation, 'r') as annotation_file, \
                    open(_latest_centerline_annotation, 'r') as centerline_file:
                _dict['Annotation time measurement'] = json.load(annotation_file)['Time measurement']
                _dict['Centerline Annotation time measurement'] = json.load(centerline_file)['Time measurement']

                # get measured lengths
                # if "VERSION_NUMBER" in _json_file.keys():
                #     _dict["measured length"] =

            _dict['Case Number'] = [int(s) for s in str(Path(di)).split('\\') if s.isdigit()][0]
            _dict['Path'] = di
            _to_csv.append(_dict)

    return _to_csv
