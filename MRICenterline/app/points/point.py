import numpy as np
from vtkmodules.all import vtkSphereSource, vtkPolyDataMapper, vtkActor

from MRICenterline.app.file_reader.AbstractReader import ImageOrientation
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline import CFG


class Point:
    def __init__(self,
                 picked_coords,
                 slice_index: int,
                 image_properties: ImageProperties or None,
                 color=(1, 1, 1),
                 size=3):

        self.image_coordinates = list(picked_coords[0:3])
        self.slice_idx = slice_index
        self.image_properties = image_properties

        self.point_color = color
        self.point_size = size
        self.point_visibility: bool = True

        self.actor = self.generate_actor()

        if self.image_properties:
            self.itk_index_coords, self.physical_coords = self.calculate_itk()

            if CFG.get_testing_status("use-slice-location"):
                z_coords = self.image_properties.z_coords
                self.image_coordinates[2] = z_coords[self.slice_idx]
        else:
            self.itk_index_coords = [0, 0, 0]
            self.physical_coords = [0, 0, 0]

    @classmethod
    def point_from_itk_index(cls, itk_coords, image_properties, color=(1, 1, 1), size=3):
        # used to load data from the internal database to the viewer
        viewer_origin = image_properties.size / 2

        image_coordinates = np.zeros(3)
        image_coordinates[0] = (itk_coords[0] - 1 - viewer_origin[0]) * image_properties.spacing[0]
        image_coordinates[1] = (itk_coords[1] - 1 - viewer_origin[1]) * image_properties.spacing[1]

        slice_idx = itk_coords[2] - 1

        image_coordinates[2] = image_properties.sitk_image.TransformIndexToPhysicalPoint([0, 0, int(slice_idx)])[1]
        return cls(image_coordinates, slice_idx, image_properties, color, size)

    @classmethod
    def point_from_v3(cls, image_coordinates, image_properties, image_orientation,
                      v3_image_size, v3_image_spacing, v3_image_dimensions, v3_z_coords,
                      color=(1, 1, 1), size=3):
        # kept for legacy purposes.
        # used to convert from the JSON-based saved points to the internal database
        viewer_origin = [i / 2.0 for i in v3_image_size]

        itk_coords = np.zeros(3, dtype=np.int32)
        itk_coords[0] = round(image_coordinates[0] / v3_image_spacing[0] + viewer_origin[0])
        itk_coords[1] = round(v3_image_dimensions[1] - (
                image_coordinates[1] / v3_image_spacing[1] + viewer_origin[1]))

        if image_orientation == ImageOrientation.CORONAL:
            itk_coords[2] = np.argmin(np.abs(np.array(v3_z_coords) - image_coordinates[2]))

            slice_index = itk_coords[2] + 2
        elif image_orientation == ImageOrientation.AXIAL:
            itk_coords[2] = v3_image_dimensions[2] - np.argmin(np.abs(np.array(v3_z_coords) - image_coordinates[2]))

            slice_index = itk_coords[2]
        else:
            # We don't have sagittal cases for now
            itk_coords[2] = 0
            slice_index = 0

        assert all([0 <= i for i in itk_coords]), "ITK coords must be positive"
        assert all([itk_coords[i] <= image_properties.size[i] for i in range(3)]), \
            "ITK coords must not be greater than the image size"

        return cls(picked_coords=image_coordinates,
                   slice_index=slice_index,
                   image_properties=image_properties,
                   color=color,
                   size=size)

    @classmethod
    def point_from_vtk_coords(cls, image_coordinates, image_properties, color=(1, 1, 1), size=3, v3_to_v4=False):
        slice_idx = int(np.argmin(np.abs(np.array(image_properties.z_coords) - image_coordinates[2])))
        return cls(image_coordinates, slice_idx, image_properties, color, size)

    def generate_actor(self):
        source = vtkSphereSource()
        source.SetCenter(self.image_coordinates[0], self.image_coordinates[1], 0)
        source.SetRadius(self.point_size/2)

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
        self.point_size = size

    def distance(self, other):
        if self.image_properties:
            c = np.array([((a - b) ** 2) for a, b, in zip(self.physical_coords, other.physical_coords)])
        else:
            c = np.array([((a - b) ** 2) for a, b, in zip(self.image_coordinates, other.image_coordinates)])

        return np.sqrt(np.sum(c))

    def __getitem__(self, item):
        if self.image_properties:
            return self.physical_coords[item]
        else:
            return self.image_coordinates[item]

    def __repr__(self):
        return f"""
            ITK Physical Coordinates: {str([i for i in self.physical_coords])}
            ITK Index Coordinates: {str([i for i in self.itk_index_coords])}
            Image coordinates: {self.image_coordinates[0]}, {self.image_coordinates[1]}
            Picked Slice index: {self.slice_idx}
        """

    def __eq__(self, other):
        return all([self.physical_coords[i] == other.physical_coords[i] for i in range(3)])

    def calculate_itk(self):
        if CFG.get_testing_status("use-slice-location"):
            viewer_origin = [i / 2.0 for i in self.image_properties.size]

            itk_coords = np.zeros(3, dtype=np.int32)
            itk_coords[0] = round(self.image_coordinates[0] / self.image_properties.spacing[0] + viewer_origin[0])
            itk_coords[1] = round(self.image_properties.dimensions[1] - (
                        self.image_coordinates[1] / self.image_properties.spacing[1] + viewer_origin[1]))
            itk_coords[2] = np.argmin(np.abs(np.array(self.image_properties.z_coords) - self.image_coordinates[2]))

        else:
            viewer_origin = self.image_properties.size / 2.0

            itk_coords = np.zeros(3, dtype=np.int32)
            itk_coords[0] = 1 + round((self.image_coordinates[0] / self.image_properties.spacing[0]) + viewer_origin[0])
            itk_coords[1] = 1 + round((self.image_coordinates[1] / self.image_properties.spacing[1]) + viewer_origin[1])
            # itk_coords[2] = 1 + round(self.image_properties.size[2] - self.slice_idx)
            itk_coords[2] = 1 + round(self.slice_idx)

        assert all([i >= 0 for i in itk_coords]), "ITK coordinates must be positive"

        physical_coords = self.image_properties.sitk_image.TransformIndexToPhysicalPoint(
            [int(itk_coords[0]), int(itk_coords[1]), int(itk_coords[2])])
        return itk_coords, physical_coords
