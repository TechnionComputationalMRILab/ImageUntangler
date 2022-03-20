import vtkmodules.all as vtk


def generate_spline(points, color=(0, 1, 0), width=4):

    pts = vtk.vtkPoints()
    [pts.InsertNextPoint(i.image_coordinates) for i in points]

    outSpline = vtk.vtkParametricSpline()
    outSpline.SetPoints(pts)

    functionSource = vtk.vtkParametricFunctionSource()
    functionSource.SetParametricFunction(outSpline)

    spline_mapper = vtk.vtkPolyDataMapper()
    spline_mapper.SetInputConnection(functionSource.GetOutputPort())

    spline_actor = vtk.vtkActor()
    spline_actor.SetMapper(spline_mapper)
    spline_actor.GetProperty().SetColor(color)
    spline_actor.GetProperty().SetLineWidth(width)

    return spline_actor

