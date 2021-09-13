import vtkmodules.all as vtk


def generate_lines(points, color, width):

    pts = vtk.vtkPoints()
    [pts.InsertNextPoint(i.image_coordinates) for i in points]

    lines_poly_data = vtk.vtkPolyData()
    lines_poly_data.SetPoints(pts)

    line_array = []

    for i in range(len(points)):
        for j in range(len(points)):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, j)
            line_array.append(line)

    lines = vtk.vtkCellArray()
    [lines.InsertNextCell(i) for i in line_array]
    lines_poly_data.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(lines_poly_data)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetLineWidth(width)

    return actor


def generate_ordered_line():
    pass
