import numpy as np
from vtkmodules.all import vtkSphereSource, vtkPolyDataMapper, vtkActor

from MRICenterline.app.gui_data_handling.image_properties import ImageProperties


class Point:
    def __init__(self,
                 picked_coords,
                 slice_index: int,
                 image_properties: ImageProperties,
                 color=(1, 1, 1),
                 size=3):
        self.image_coordinates = picked_coords[0:3]
        self.slice_idx = slice_index
        self.image_properties = image_properties

        self.point_color = color
        self.point_size = size
        self.point_visibility: bool = True

        self.actor = self.generate_actor()
        self.itk_index_coords, self.physical_coords = self.calculate_itk()

    @classmethod
    def point_from_physical(cls, physical_coords, image_properties, color=(1, 1, 1), size=3):
        pass #TODO

    def generate_actor(self):
        source = vtkSphereSource()
        source.SetCenter(self.image_coordinates[0], self.image_coordinates[1], 0)
        source.SetRadius(self.point_size)

        # Create a mapper
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # Create an panel_actor
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(self.point_color)
        actor.GetProperty().SetDiffuse(1)
        actor.GetProperty().SetSpecular(1)

        return actor

    def set_visibility(self, visibility: bool):
        self.point_visibility = visibility
        self.actor.SetVisibility(visibility)

    def get_actor(self):
        return self.actor

    def set_color(self, color):
        self.actor.GetProperty().SetColor(color)
        self.point_color = color

    def set_size(self, size):
        self.point_size = size if size >= 4 else 4

    def distance(self, other):
        c = np.array([((a - b) ** 2) for a, b, in zip(self.physical_coords, other.physical_coords)])
        return np.sqrt(np.sum(c))
        # return np.linalg.norm(self - other)

    def __repr__(self):
        return f"""
            ITK Physical Coordinates: {str([i for i in self.physical_coords])}
            ITK Index Coordinates: {str([i for i in self.itk_index_coords])}
        """

    def calculate_itk(self):
        viewer_origin = self.image_properties.size / 2.0

        itk_index_x = round(self.image_coordinates[0]/self.image_properties.spacing[0] + viewer_origin[0])
        itk_index_y = round(self.image_properties.size[1] - (self.image_coordinates[1] / self.image_properties.spacing[1] + viewer_origin[1]))
        itk_index_z = self.slice_idx
        itk_index = (int(itk_index_x), int(itk_index_y), int(itk_index_z))

        physical_coords = self.image_properties.sitk_image.TransformIndexToPhysicalPoint(itk_index)
        return itk_index, physical_coords
