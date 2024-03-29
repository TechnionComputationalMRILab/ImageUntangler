from enum import Enum


class ImageOrientation(Enum):
    CORONAL = "C"
    AXIAL = "A"
    SAGITTAL = "S"
    UNKNOWN = "U"


class AbstractReader:
    def __init__(self, case_id: int, case_name: str, folder: str, is_new_case: bool = False):
        self.case_id = case_id
        self.case_name = case_name
        self.folder = folder
        self.sitk_image = None
        self.is_new_case = is_new_case

        self.sequence_list = []

    def get_sequences(self):
        return self.sequence_list

    def __getitem__(self, item):
        raise NotImplementedError

    def __len__(self):
        return len(self.sequence_list)

    def get_image_orientation(self, item) -> ImageOrientation:
        raise NotImplementedError

