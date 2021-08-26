import os
from MRICenterline.FileReaders.DICOMReader import DICOMReader


def get_directories(folder):
    _folders = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in dirs:
            _full_path = os.path.join(root, name)
            _folders.append(_full_path)

    return _folders


def generate_seq_dict(folder):
    _dicomreader = DICOMReader.test_folder(folder)
    if _dicomreader is type(DICOMReader):
        if _dicomreader.check_seqfile_exists():
            _dicomreader.generate_seq_dict()
