from typing import List

from util.MRI_files import get_directory


class DICOMSequence:
    def __init__(self, slices: List[str], name: str):
        self.slices = slices
        self.name = name
        self.last_index = -1

    def max_index(self) -> int:
        return len(self.slices)-1

    def get_index(self) -> int:
        return self.last_index

    def get_middle_slice(self) -> str:
        self.last_index = len(self.slices)//2
        return self.slices[self.last_index]
    
    def get_current_slice(self) -> str:
        return self.slices[self.last_index]

    def increment(self) -> str:
        if self.last_index != len(self.slices)-1:
            self.last_index+=1
        return self.slices[self.last_index]

    def decrement(self):
        if self.last_index != len(self.slices)-1:
            self.last_index-=1
        return self.slices[self.last_index]

    def get_slice(self, index: int):
        self.last_index = index
        return self.slices[self.last_index]

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.slices)

    @staticmethod
    def get_dicom_seqs(all_slices: List[str]):
        """
        :param all_slices: list of all paths to dicom images (collection of slices mashed together)
        :return: DICOM Sequences, each containing their relevant slices
        """
        all_sequences: List[DICOMSequence] = []
        last_file_dir = ''
        current_seq = []
        for file in sorted(all_slices):
            current_directory = get_directory(file)
            if current_directory == last_file_dir:
                current_seq.append(file)
            else:
                if len(current_seq) > 0:
                    all_sequences.append(DICOMSequence(current_seq, name=last_file_dir))
                last_file_dir = current_directory
                current_seq = []
        all_sequences.append(DICOMSequence(current_seq, name=last_file_dir))
        return all_sequences