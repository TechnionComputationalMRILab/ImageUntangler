import SimpleITK as sitk
import numpy as np

from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties


class CenterlineImageProperties(ImageProperties):
    def __init__(self,
                 mpr_np_array: np.ndarray,
                 input_image_properties: ImageProperties):
        self.mpr_np_array = mpr_np_array

        mpr_img = sitk.GetImageFromArray(mpr_np_array)
        mpr_img.SetSpacing(input_image_properties.spacing)

        super().__init__(sitk_image=mpr_img,
                         image_orientation=ImageOrientation.UNKNOWN,
                         z_coords=[])

    def get_vtk_data(self):
        from vtkmodules.all import vtkImageData, VTK_TYPE_UINT16
        from vtkmodules.util import numpy_support

        mpr_m = self.mpr_np_array
        delta = self.spacing[0]

        n = mpr_m.shape[0]
        m = mpr_m.shape[1]

        image_data = vtkImageData()
        image_data.SetDimensions(m, n, 1)
        image_data.SetOrigin(0, 0, 0)

        image_data.SetSpacing(delta, delta, delta)

        scalars = numpy_support.numpy_to_vtk(num_array=mpr_m.ravel(), deep=True, array_type=VTK_TYPE_UINT16)

        image_data.GetPointData().SetScalars(scalars)
        image_data.Modified()

        return image_data
