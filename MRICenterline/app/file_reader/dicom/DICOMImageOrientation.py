from MRICenterline.app.file_reader.dicom import constants
from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
import SimpleITK as sitk

import logging
logging.getLogger(__name__)


def get_image_orientation(file) -> ImageOrientation:
    reader = sitk.ImageFileReader()

    reader.SetFileName(file)
    reader.LoadPrivateTagsOn()

    try:
        reader.ReadImageInformation()
    except Exception as e:
        logging.info(f"Get image orientation failed on file {file} | {e}")
    else:
        for k in reader.GetMetaDataKeys():
            v = reader.GetMetaData(k)

            tag1, tag2 = k.split("|")

            if len(v) and tag1 == "0020" and tag2 == "0037":
                image_orientation = [round(float(i)) for i in v.split("\\")]

                if image_orientation == constants.CORONAL:
                    return ImageOrientation.CORONAL
                elif image_orientation == constants.AXIAL:
                    return ImageOrientation.AXIAL
                elif image_orientation == constants.SAGITTAL:
                    return ImageOrientation.SAGITTAL

    return ImageOrientation.UNKNOWN
