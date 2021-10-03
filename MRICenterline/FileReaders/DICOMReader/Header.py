# from icecream import ic
from pydicom.errors import InvalidDicomError

from . import SequenceFile

FOR_USE_WITH_HEADER = ['StudyTime',
                       'AcquisitionTime',
                       'StudyDescription',
                       'SeriesDescription',
                       'PatientAge',
                       'PatientBirthDate',
                       'PatientID',
                       'PatientName',
                       'PatientPosition',
                       'PatientSex',
                       'PatientWeight']


def get_sequence_header(header_name, list_of_files):
    _headers = [SequenceFile.get_info(header_name, file, get_one=True) for file in list_of_files]
    if len(set(_headers)) == 1:
        return _headers[0]
    else:
        raise InvalidDicomError


def get_header_dict(file_list):
    _dict = dict()
    _dict['filename'] = file_list

    for key in FOR_USE_WITH_HEADER:
        try:
            _dict[key] = get_sequence_header(key, file_list)
        except:
            _dict[key] = ""
    return _dict
