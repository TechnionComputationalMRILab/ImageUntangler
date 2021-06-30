import math
from vtkmodules.all import vtkNrrdReader, vtkDICOMImageReader
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.util import numpy_support

import nrrd
import pydicom as dicom
from icecream import ic
import numpy as np
ic.configureOutput(includeContext=True)
from util import ConfigRead as CFG, logger
logger = logger.get_logger()


def getImageData(imgPath: str, isDicom, imager):
    if CFG.get_testing_status('reader-reimplementation'):
        # TODO: get the vtkImageData from the Imager
        pass

    else:
        return old_getImageData(imgPath, isDicom)

def old_getImageData(imgPath, isDicom):
    if isDicom:
        reader = vtkDICOMImageReader()

        with open(imgPath, 'rb') as infile:
            dcmr = dicom.dcmread(infile)

            header = dict()

        header['file type'] = 'dicom'
    else:
        reader = vtkNrrdReader()

        with open(imgPath, 'rb') as infile:
            header = nrrd.read_header(infile)

        header["file type"] = "nrrd"

    reader.SetFileName(imgPath)
    reader.Update()
    imageData = reader.GetOutput()

    header['filename'] = imgPath
    return ImageProperties(imageData, header)


class ImageProperties: # class makes operations more efficient by caching image data in memory
    def __init__(self, fullData: vtkImageData, header: dict):
        self.fullData = fullData # ??temp
        self.spacing = fullData.GetSpacing()
        self.dimensions = fullData.GetDimensions()
        self.extent = fullData.GetExtent()
        self.origin = fullData.GetOrigin()
        center_z = self.origin[2] + self.spacing[2] * 0.5 * (self.extent[4] + self.extent[5])
        self.sliceIdx = math.ceil((center_z-self.origin[2]) / self.spacing[2])
        self.dicomArray = numpy_support.vtk_to_numpy(fullData.GetPointData().GetArray(0))
        self.dicomArray = self.dicomArray.reshape(self.dimensions, order='F')

        self.header = header

        min_z = round(center_z - (self.origin[2] + self.spacing[2] * (self.dimensions[2])), 1)
        max_z = math.floor((self.dimensions[2] * self.spacing[2]) + min_z)
        self.slice_list = dict(zip(np.arange(self.dimensions[2]), np.arange(min_z, max_z, self.spacing[2])))

    def getParallelScale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])

    def convertZCoordsToSlices(self, z_coords: list):
        _slice_list = []
        for i in z_coords:
            for k, v in self.slice_list.items():
                # if np.isclose(i, v):
                #     _slice_list.append(k)
                if round(i, 3) == round(v, 3):
                    _slice_list.append(k)

        return _slice_list
