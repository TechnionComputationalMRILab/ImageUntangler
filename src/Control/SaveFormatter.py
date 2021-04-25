import nrrd
import pydicom as dicom
import json


ACCEPTABLE_FILE_TYPES = ['csv', 'json', 'sqllite', 'mysql', 'hdf5']
NOT_IMPLEMENTED = ['csv', 'sqllite', 'mysql', 'hdf5']


class SaveFormatter:
    def __init__(self, input_file, data_to_save, output_file):
        self.in_file = input_file
        self.data = data_to_save
        self.out_type = output_file

        if self.out_type.lower() in NOT_IMPLEMENTED:
            raise NotImplementedError(f"Output to format {self.out_type} will be implemented in a future release")
        elif self.out_type.lower() not in ACCEPTABLE_FILE_TYPES:
            raise NotImplementedError(f'There are currently no plans to support {self.out_type} type output')
        else:
            self.header = self.read_input_file()

    def read_input_file(self):
        try:
            # try opening the file as a NRRD file
            with open(self.in_file, 'rb') as infile:
                header = nrrd.read_header(infile)
        except nrrd.errors.NRRDError:
            raise NotImplementedError

        return header

    def save_header(self):
        pass

    def save_data(self):
        if self.out_type.lower() == 'json':
            pass
        elif self.out_type.lower() == "csv":
            # do something else
            raise NotImplementedError
        else:
            raise NotImplementedError