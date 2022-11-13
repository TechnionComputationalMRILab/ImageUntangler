import SimpleITK as sitk
import numpy as np

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.points.point import Point


class Point2D(Point):
    def __init__(self,
                 picked_coords,
                 image_properties: ImageProperties or None,
                 color=(1, 1, 1),
                 size=3):
        super().__init__(
            picked_coords=picked_coords,
            slice_index=0,
            image_properties=image_properties,
            color=color,
            size=size)

        self.image_coordinates = list(picked_coords[0:2])
        self.image_coordinates.append(0)  # fake 3rd dimension so that get_vertical_distance will work

    def calculate_itk(self):
        itk_coords = np.zeros(2, dtype=np.int32)

        itk_coords[0] = 1 + round((self.image_coordinates[0] / self.image_properties.spacing[0]))
        itk_coords[1] = 1 + round((self.image_coordinates[1] / self.image_properties.spacing[1]))

        assert all([itk_coords[i] <= self.image_properties.size[i] for i in range(2)]), \
            "ITK coords must not be greater than the image size"

        physical_coords = self.image_properties.sitk_image.TransformIndexToPhysicalPoint(
            [int(itk_coords[0]), int(itk_coords[1])])

        return itk_coords, physical_coords

    def __repr__(self):
        return f"""
            ITK Physical Coordinates: {str([i for i in self.physical_coords])}
            ITK Index Coordinates: {str([i for i in self.itk_index_coords])}
            Image coordinates: {self.image_coordinates[0]}, {self.image_coordinates[1]}
        """

    def __eq__(self, other):
        return all([self.physical_coords[i] == other.physical_coords[i] for i in range(2)])

    @classmethod
    def point_from_itk_index(cls, itk_coords, image_properties, color=(1, 1, 1), size=3):
        # used to load data from the internal database to the viewer
        viewer_origin = image_properties.size / 2

        image_coordinates = np.zeros(2)
        image_coordinates[0] = (itk_coords[0] - 1) * image_properties.spacing[0]
        image_coordinates[1] = (itk_coords[1] - 1) * image_properties.spacing[1]

        return cls(image_coordinates, image_properties, color, size)
