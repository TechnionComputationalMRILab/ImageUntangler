import os
import pydicom
from typing import List
import json
import numpy as np
import copy


from util import logger
logger = logger.get_logger()

"""
several functions for use with DICOMReader class
implemented in a separated file just in case a similar file needs to be made
to group DICOM files based on PatientIDs or other DICOM keys
"""


def check_if_dicom_seqfile_exists(path):
    """
    looks for a json file in the directory
    to implement: make sure that the json file is the seqfile and not some other json file
    """
    for file in os.listdir(path):
        if file.endswith(".json"):
            return file
    else:
        return None


def load_seqfile(folder, seqfile):
    with open(os.path.join(folder, seqfile), 'r') as f:
        sequence_file = json.load(f)
    sequence_dict = {k: [os.path.join(folder, i) for i in v] for k, v in sequence_file.items()}

    return sequence_dict


def create_sequence_file(files: List[str]):
    """
    creates, saves, and returns a sequence file to be used by DICOMReader
    """
    grouped_files = _groupby(files, lambda x: _get_info('SeriesDescription', x),
                             include_path_key=True, include_path_in_list=False)
    copy_grouped_files = copy.deepcopy(grouped_files)

    path = grouped_files.pop("Path")[0]
    filename = _get_seqfile_filename(files)

    with open(os.path.join(path, filename), 'w') as f:
        json.dump(grouped_files, f, indent=4, sort_keys=True)

    return copy_grouped_files


def _groupby(files: List[str], func,
             include_path_key=False, include_path_in_list=True):
    """
    groups the files in the list by grouping it based on a DICOM key
    """
    paths, _ = zip(*[os.path.split(f) for f in files])
    _images_and_series_desc = files.copy()

    for i, s in enumerate(_images_and_series_desc):
        _images_and_series_desc[i] = func(s)

    _sequences = list(set(_images_and_series_desc))
    _images_and_series_desc = np.stack([files, _images_and_series_desc], axis=1)
    _grouped_sequences = [_images_and_series_desc[_images_and_series_desc[:, -1] == seq][:, 0]
                          for seq in _sequences]

    _sequence_dict = {v: list(_grouped_sequences[k]) for k, v in enumerate(_sequences)}

    if not include_path_in_list:
        _sequence_dict = {k: [os.path.basename(i) for i in v] for k, v in _sequence_dict.items()}
    if include_path_key:
        _sequence_dict["Path"] = list(set(paths))

    return _sequence_dict


def _get_info(header_name, filename, get_one=True):
    """
    uses pydicom's dir() method to get additional information from the header
    ex: header_name = 'patient' returns a dict with all keys with the word
    'patient' in it

    alternatively, returns only one string according to a DICOM key, to be
    used with _groupby
    """
    with open(filename, 'rb') as f:
        ds = pydicom.dcmread(f)
    if get_one:
        return str(ds[header_name].value)
    else:
        return {i: ds[i].value for i in ds.dir(header_name)}


def _get_seqfile_filename(files):
    """
    generates a filename for the sequence directory file
    """
    paths = [os.path.dirname(os.path.abspath(file)) for file in files]
    if len(set(paths)) == 1:
        _seq_filename = os.path.basename(paths[0]) + "_sequence_directory.json"
        return _seq_filename
    else:
        raise NotImplementedError("Program does not yet work for data in nested folders")
