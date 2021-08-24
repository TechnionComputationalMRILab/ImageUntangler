import vtkmodules.all as vtk


def test_actor(rad):
    colors = vtk.vtkNamedColors()

    # Create a circle
    polygonSource = vtk.vtkRegularPolygonSource()
    # Comment this line to generate a disk instead of a circle.
    polygonSource.GeneratePolygonOff()
    polygonSource.SetNumberOfSides(50)
    polygonSource.SetRadius(rad)
    polygonSource.SetCenter(0.0, 0.0, 0.0)

    #  Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(polygonSource.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Cornsilk'))

    return actor
