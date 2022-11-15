import SimpleITK as sitk
import numpy as np

from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point_array import PointArray
from MRICenterline import CFG, MSG

import logging
logging.getLogger(__name__)


class CenterlineImageProperties(ImageProperties):
    def __init__(self,
                 mpr_np_array: np.ndarray,
                 input_image_properties: ImageProperties):
        self.mpr_np_array = mpr_np_array

        mpr_img = sitk.GetImageFromArray(mpr_np_array)
        mpr_img.SetSpacing([input_image_properties.spacing[1], input_image_properties.spacing[0], 1])

        super().__init__(sitk_image=mpr_img,
                         image_orientation=ImageOrientation.UNKNOWN,
                         z_coords=[])

    @classmethod
    def from_input(cls, input_points: PointArray, height, angle, input_image):
        from MRICenterline.app.centerline.calculate import get_straight_mpr

        np_pts = input_points.get_as_array_for_centerline(input_image)
        mpr_np = np.zeros(1)

        if CFG.get_testing_status("running-for-tests"):
            mpr_np = get_straight_mpr(img=input_image, points=np_pts, xRad=height,
                                      viewAngle=angle)
        else:
            try:
                mpr_np = get_straight_mpr(img=input_image, points=np_pts, xRad=height,
                                          viewAngle=angle)
            except Exception as e:
                MSG.msg_box_warning(f'Error in calculating centerline: {e}')
                logging.warning(f'Error in calculating centerline: {e}')

        return cls(mpr_np, input_image)

    def get_parallel_scale(self):
        return self.spacing[0] * (self.extent[1] - self.extent[0])

    def get_vtk_data(self):
        from vtkmodules.all import vtkImageData, VTK_TYPE_UINT16
        from vtkmodules.util import numpy_support

        mpr_m = self.mpr_np_array

        n = mpr_m.shape[0]
        m = mpr_m.shape[1]

        image_data = vtkImageData()
        image_data.SetDimensions(m, n, 1)
        image_data.SetOrigin(0, 0, 0)

        image_data.SetSpacing(self.spacing[1], self.spacing[0], 1)

        scalars = numpy_support.numpy_to_vtk(num_array=mpr_m.ravel(), deep=True, array_type=VTK_TYPE_UINT16)

        image_data.GetPointData().SetScalars(scalars)
        image_data.Modified()

        return image_data
