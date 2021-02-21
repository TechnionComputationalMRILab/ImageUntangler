import math
from icecream import ic
from vtk import vtkNrrdReader, vtkDICOMImageReader
from vtk.util import numpy_support


def getImageData(imgPath: str, isDicom: bool):
    if isDicom:
        reader = vtkDICOMImageReader()
    else:
        reader = vtkNrrdReader()
    reader.SetFileName(imgPath)
    reader.Update()
    imageData = reader.GetOutput()
    return ImageProperties(imageData, imageData.GetSpacing(), imageData.GetDimensions(),
                                           imageData.GetExtent(), imageData.GetPointData(), imageData.GetOrigin())


class ImageProperties:
    def __init__(self, fullData, spacing, dimensions, extent, pointData, origin):
        self.fullData = fullData # ??temp
        self.spacing = spacing
        self.dimensions = dimensions
        self.extent = extent
        self.origin = origin
        center_z = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
        self.sliceIdx = math.ceil((center_z-origin[2]) / spacing[2])
        nn = pointData.GetArray(0)
        ic(type(nn))
        self.dicomArray = numpy_support.vtk_to_numpy(nn)
        self.dicomArray = self.dicomArray.reshape(dimensions, order='F')

    def getParallelScale(self):
        return 0.5 * self.spacing[0] * (self.extent[1] - self.extent[0])


