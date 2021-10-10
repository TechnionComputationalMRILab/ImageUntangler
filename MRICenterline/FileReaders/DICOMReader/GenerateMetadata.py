from os.path import join
from glob import glob
import json
from pydicom import dcmread


def get(seq_dict):
    filename = seq_dict[list(seq_dict.keys())[0]][0]
    patient_data = dcmread(filename)
    relevant_info = ['PatientName', "PatientID",
                     "Manufacturer", "ManufacturerModelName",
                     "ProtocolName",
                     "StudyDate", 'StudyTime']

    metadata_dict = {}
    for item in relevant_info:
        try:
            metadata_dict[item] = str(patient_data[item].value)
        except:
            metadata_dict[item] = " "

    return metadata_dict


def save(metadata_dict, folder):
    with open(join(folder, 'data', 'metadata.json'), 'w') as f:
        json.dump(metadata_dict, f, indent=4, sort_keys=True)


def read(folder):
    with open(join(folder, 'data', 'metadata.json'), 'w') as f:
        metadata_dict = json.load(f)
    return metadata_dict
