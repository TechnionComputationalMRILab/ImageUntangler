import os
import pydicom
from typing import List
import json
from glob import glob
import numpy as np

from MRICenterline.utils import message as MSG
import logging
logging.getLogger(__name__)

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
    if os.path.isfile(os.path.join(path, 'data', 'seqdict.json')):
        return os.path.join(path, 'data', 'seqdict.json')
    else:
        return None


def load_seqfile(folder, seqfile):
    with open(os.path.join(folder, seqfile), 'r') as f:
        sequence_file = json.load(f)
    sequence_dict = {k: [os.path.join(folder, i) for i in v] for k, v in sequence_file.items()}

    return sequence_dict


def create_sequence_file(path, seq_dict):
    # path = os.path.dirname(files[0])
    # grouped_files = generate_seqlist_dict(files)

    with open(os.path.join(path, 'data', 'seqdict.json'), 'w') as f:
        json.dump(seq_dict, f, indent=4, sort_keys=True)


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


def get_info(header_name, filename, get_one=True):
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


# def _get_seqfile_filename(files):
#     """
#     generates a filename for the sequence directory file
#     """
#     paths = [os.path.dirname(os.path.abspath(file)) for file in files]
#     if len(set(paths)) == 1:
#         _seq_filename = os.path.basename(paths[0]) + "_sequence_directory.json"
#         return _seq_filename
#     else:
#         raise NotImplementedError("Program does not yet work for data in nested folders")


def generate_seqlist_dict(files_list):
    seq_list = {}
    sorted_files = {}
    for filename in files_list:
        dicom_info = pydicom.dcmread(filename)
        _file = os.path.basename(filename)
        try:
            seq_name = dicom_info['SeriesDescription'].value
        except:
            logging.warning(f"Ignoring invalid file: {_file}")
        else:
            if seq_name:  # takes care of the blank sequence names
                if seq_name in seq_list:
                    sorted_files[seq_name][_file] = _file
                else:
                    sorted_files[seq_name] = {_file: _file}
                    seq_list[seq_name] = seq_name

    seq_list = [seq_val[1] for seq_val in seq_list.items()]
    seq_list = set(seq_list)
    seq_files_list = {}
    for seq_name in seq_list:
        seq_files_list[seq_name] = [file_entry[1] for file_entry in sorted_files[seq_name].items()]

    return seq_files_list
