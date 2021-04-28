import math
from vtk import vtkNrrdReader, vtkDICOMImageReader
from vtk.vtkCommonDataModel import vtkImageData
from vtk.util import numpy_support

import nrrd
import pydicom as dicom


def getImageData(imgPath: str, isDicom: bool):
    if isDicom:
        reader = vtkDICOMImageReader()
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

    def getParallelScale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])


