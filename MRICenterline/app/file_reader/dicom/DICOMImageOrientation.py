from MRICenterline.app.file_reader.dicom import constants
from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
import SimpleITK as sitk


def get_image_orientation(file) -> ImageOrientation:
    reader = sitk.ImageFileReader()

    reader.SetFileName(file)
    reader.LoadPrivateTagsOn()

    reader.ReadImageInformation()

    for k in reader.GetMetaDataKeys():
        v = reader.GetMetaData(k)

        tag1, tag2 = k.split("|")

        if tag1 == "0020" and tag2 == "0037":
            image_orientation = [round(float(i)) for i in v.split("\\")]

            if image_orientation == constants.CORONAL:
                return ImageOrientation.CORONAL
            elif image_orientation == constants.AXIAL:
                return ImageOrientation.AXIAL
            elif image_orientation == constants.SAGITTAL:
                return ImageOrientation.SAGITTAL
            else:
                return ImageOrientation.UNKNOWN
