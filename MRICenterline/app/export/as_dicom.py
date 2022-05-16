import SimpleITK as sitk

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point_array import PointArray


def export_as_dicom(image_properties: ImageProperties, mpr_points: PointArray, length_points: PointArray):
    itk_image = image_properties.sitk_image

    # TOOO the actual export
