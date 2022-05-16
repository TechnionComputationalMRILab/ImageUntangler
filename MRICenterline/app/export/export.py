from enum import Enum, auto
import numpy as np

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.export.as_dicom import export_as_dicom


class ExportType(Enum):
    DICOM = auto()
    IPYNB = auto()
    PNG = auto()


def export(image_properties: ImageProperties, mpr_points: PointArray, length_points: PointArray):
    """ Assigns the export from the SequenceModel to the appropriate function """

    # save these as CSV files
    mpr_display_points = convert_point_array_to_list(mpr_points, output="IMAGE")
    mpr_itk_indices = convert_point_array_to_list(mpr_points, output="ITK_IDX")

    length_display_points = convert_point_array_to_list(length_points, output="IMAGE")
    length_itk_indices = convert_point_array_to_list(mpr_points, output="ITK_IDX")

    export_as_dicom(image_properties, mpr_points, length_points)


def convert_point_array_to_list(array: PointArray, output: str = "ITK_IDX") -> np.ndarray:
    converted_list = np.zeros((len(array), 3))
    for idx, pt in enumerate(array):
        if output == "ITK_IDX":
            converted_list[idx:] = np.array(pt.itk_index_coords)
        elif output == "IMAGE":
            converted_list[idx:] = np.array(pt.image_coordinates)
        elif output == "ITK_PHYSICAL":
            converted_list[idx:] = np.array(pt.physical_coords)
        else:
            raise KeyError

    return converted_list
