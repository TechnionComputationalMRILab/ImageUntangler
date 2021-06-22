import psutil, os
from DICOMReader import DICOMReader

absolute_path = "C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\enc_files\\"
test_dicom_reader = DICOMReader(absolute_path)

# print(test_dicom_reader.get_sequence_list())


def test_caching():
    print("initial memory used")
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("loading '3 plane Loc SSFSE BH'")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("reloading '3 plane Loc SSFSE BH' from cache, should be minimal change from above")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("loading 'Ax 2D FIESTA'")
    test_dicom_reader['Ax 2D FIESTA']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("reloading '3 plane Loc SSFSE BH' from cache, should be minimal change from above")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
