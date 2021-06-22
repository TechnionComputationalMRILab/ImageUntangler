from DICOMReader import DICOMReader

absolute_path = "C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\enc_files\\"
test_dicom_reader = DICOMReader(absolute_path)

print(test_dicom_reader.sequence_dict)