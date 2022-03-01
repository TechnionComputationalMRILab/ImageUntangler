import numpy as np


class AbstractReader:
    def __init__(self, case_id: int, folder: str, is_new_case: bool = False):
        self.case_id = case_id
        self.folder = folder
        self.sitk_image = None
        self.is_new_case = is_new_case

        self.sequence_list = []

    def get_sequences(self):
        return self.sequence_list

    def __getitem__(self, item) -> np.ndarray:
        raise NotImplementedError

    def __len__(self):
        return len(self.sequence_list)
