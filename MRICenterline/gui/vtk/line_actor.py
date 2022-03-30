import vtkmodules.all as vtk


def generate_line_actor(point_a, point_b, color=(1, 0, 0), width=2):
    pts = vtk.vtkPoints()
    pts.InsertNextPoint(point_a)
    pts.InsertNextPoint(point_b)

    lines_poly_data = vtk.vtkPolyData()
    lines_poly_data.SetPoints(pts)

    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, 1)
    line.GetPointIds().SetId(1, 2)

    lines = vtk.vtkCellArray()
    lines.InsertNextCell(line)
    lines_poly_data.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(lines_poly_data)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetLineWidth(width)

    return actor
