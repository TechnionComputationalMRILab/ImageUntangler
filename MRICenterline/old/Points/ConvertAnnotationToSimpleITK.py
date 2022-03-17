import SimpleITK as sitk
import vtkmodules.all as vtk
import numpy as np


def func(input_points, viewport, dicom_folder, slice_index):
    coord = vtk.vtkCoordinate()
    print("\n")
    print(f'Input points: {input_points}')
    print(f'Coordinate system: {coord.GetCoordinateSystemAsString()}')

    # # coord.SetViewport(viewport)
    # coord.SetValue(input_points[0], input_points[1], input_points[2])
    #
    # tra = vtk.vtkTransformCoordinateSystems()

    cam = viewport.GetActiveCamera()
    halfheight = cam.GetParallelScale()

    image = get_sitk_image(dicom_folder)

    xlist = np.linspace(-halfheight, halfheight, num=image.GetWidth())
    ylist = np.linspace(-halfheight, halfheight, num=image.GetHeight())
    x_idx = find_nearest(xlist, input_points[0])
    y_idx = image.GetHeight()-find_nearest(ylist, input_points[1])
    indices = [int(x_idx), int(y_idx), int(slice_index)]

    print(f'Indices {indices}')

    try:
        # physical_coords = image.TransformIndexToPhysicalPoint(indices)
        physical_coords = image.TransformContinuousIndexToPhysicalPoint(indices)
    except Exception as e:
        print(f'Err: {e}')
    else:
        print(f'Converted physical coords: {physical_coords[0], physical_coords[1]-image.GetSpacing()[2], physical_coords[2]}')
        # print(f'Converted physical coords: {physical_coords}')

        return physical_coords[0], physical_coords[1]-image.GetSpacing()[2], physical_coords[2]


def get_sitk_image(folder):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(folder)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    dir = np.array(image.GetDirection()).reshape(3, 3)
    print(dir)
    return image

    # nda = sitk.GetArrayFromImage(image)
    # nda = np.flipud(nda)
    # nda.shape


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
