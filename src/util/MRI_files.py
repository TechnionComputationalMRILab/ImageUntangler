import pydicom
import nrrd
from typing import List
import os

from util import logger
logger = logger.get_logger()


def get_directory(path: str) -> str:
    return path[:path.rfind(os.path.sep)]


def combineFormats(images: List[str]) -> bool:
    hasNRRD = False
    hasDICOM = False
    for i in range(len(images) - 1):
        if isValidNrrd(images[i]):
            hasNRRD = True
        elif isValidDicom(images[i]):
            hasDICOM = True
    return (hasNRRD and hasDICOM)


def isValidNrrd(filename: str):
    try:
        with open(filename, 'rb') as infile:
            header = nrrd.read_header(infile)
    except:
        return False
    else:
        return True


def isValidDicom(filename: str):
    try:
        with open(filename, 'rb') as infile:
            ds = pydicom.dcmread(infile)
    except:
        return False
    else:
        return True


def getMRIimages(directory: str) -> List[str]:
    # returns list of all .nrrd files in directories/subdirectories
    allFiles = os.listdir(directory)
    logger.info(f"Opening directory: {directory}")
    MRIimages = list()
    for entry in allFiles:
        fullPath = os.path.join(directory, entry)
        # logger.debug(f'Adding to file list: {entry}')
        if os.path.isdir(fullPath):
            MRIimages = MRIimages + getMRIimages(fullPath)
        else:
            if isValidNrrd(fullPath):
                MRIimages.append(fullPath)
            elif isValidDicom(fullPath):
                MRIimages.append(fullPath)
    if combineFormats(MRIimages):
        raise ValueError("DO NOT COMBINE DICOM AND NRRD FILES FOR A SINGLE PATIENT")

    return MRIimages
