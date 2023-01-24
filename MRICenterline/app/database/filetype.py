"""
Reads a directory and identifies the type of the files using sitk
"""

import pydicom
import SimpleITK as sitk
from pathlib import Path
from glob import glob
sitk.ProcessObject_SetGlobalWarningDisplay(False)


def read_as_dicom_directory(folder):
    try:
        reader = sitk.ImageSeriesReader()
        files = reader.GetGDCMSeriesFileNames(folder)
        reader.SetFileNames(files)
        reader.Execute()
    except:
        return False
    else:
        return True


def read_as_dicom_files(files):
    found = False
    for f in files:
        if Path(f).name.split(".")[-1] == "dcm":
            try:
                pydicom.dcmread(f)
            except:
                found = False
                continue
            else:
                found = True
                break

    return found


def read_as_nrrd(file):
    try:
        reader = sitk.ImageFileReader()
        reader.SetFileName(file)
        reader.Execute()
    except:
        return False
    else:
        return True


def read_folder(inp):
    """
    reads a folder and checks if simpleITK can read it as either an NRRD or DICOM file

    :param inp: input, can be a folder or a file
    :return:
    """
    if type(inp) is not str:
        inp = str(inp)

    if Path(inp).is_file() and read_as_nrrd(inp):
        return 'NRRD'
    elif Path(inp).is_dir():
        files = [file for file in glob(f'{inp}/*') if not file == "metadata.db"]

        if len(files) > 1 and read_as_dicom_directory(inp):
            return 'DICOM'
        elif len(files) == 1 and read_as_nrrd(files[0]):
            return 'NRRD'
        elif len(files) > 1 and read_as_dicom_files(files):
            return "DICOM"
        else:
            return 'INVALID'
    else:
        return 'INVALID'


if __name__ == "__main__":
    has_no_valid_files = r'C:\Users\ang.a\OneDrive - Technion\Documents\OneNote Notebooks\My Notebook'
    empty_dir = r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\01002\01002\reports'
    multiple_dicom_dir = r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\test_dir\1'
    single_dicom_dir = r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\test_dir\2'
    mrrd_dir =  r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\Case005\Case006\NRRDS\003_AXIAL_TRUFISP_2D_UPPER'

    print(multiple_dicom_dir)
    print(type(multiple_dicom_dir))
    print(read_folder(multiple_dicom_dir))
    # print(read_as_dicom_directory(single_dicom_dir))
