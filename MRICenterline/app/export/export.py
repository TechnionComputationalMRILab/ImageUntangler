import os
import csv
from enum import Enum, auto
import numpy as np

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point_array import PointArray
from MRICenterline.app.export.as_dicom import export_as_dicom

import logging
logging.getLogger(__name__)


class ExportType(Enum):
    DICOM = "DICOM"
    PNG = "PNG"
    NPZ = "NPZ"


def export(image_properties: ImageProperties,
           mpr_points: PointArray, length_points: PointArray,
           case_id: int, seq_id: int,
           destination):
    """ Assigns the export from the SequenceModel to the appropriate function """
    logging.info(f"Exporting {case_id} / {seq_id} to FORMAT")

    # save these as CSV files
    mpr_display_points = convert_point_array_to_list(mpr_points, output="IMAGE")
    mpr_itk_indices = convert_point_array_to_list(mpr_points, output="ITK_IDX")

    length_display_points = convert_point_array_to_list(length_points, output="IMAGE")
    length_itk_indices = convert_point_array_to_list(mpr_points, output="ITK_IDX")

    def write(array, filename):
        with open(os.path.join(destination, filename), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=",")
            for row in array:
                writer.writerow(row)

    write(mpr_display_points, "mpr_image.csv")
    write(mpr_itk_indices, "mpr_itk_index.csv")
    write(length_display_points, "length_image.csv")
    write(length_itk_indices, "length_itk_index.csv")

    export_as_dicom(case_id, seq_id, destination)


def convert_point_array_to_list(array: PointArray, output: str = "ITK_IDX") -> np.ndarray:
    converted_list = np.zeros((len(array), 3))
    for idx, pt in enumerate(array):
        if output == "ITK_IDX":
            converted_list[idx, :] = np.array(pt.itk_index_coords)
        elif output == "IMAGE":
            converted_list[idx, :] = np.array(pt.image_coordinates)
        elif output == "ITK_PHYSICAL":
            converted_list[idx, :] = np.array(pt.physical_coords)
        else:
            raise KeyError

    return converted_list
