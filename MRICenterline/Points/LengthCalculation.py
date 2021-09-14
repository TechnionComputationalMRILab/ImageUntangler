import numpy as np
import vtkmodules.all as vtk


def length_actor(length_array, color=(0, 1, 1)):
    p1 = length_array[0]
    p2 = length_array[1]
    length = round(length_array[2], 2)
    midpoint = (p1+p2).int_div(2)

    atext = vtk.vtkVectorText()
    atext.SetText(str(length))
    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(atext.GetOutputPort())
    textActor = vtk.vtkFollower()
    textActor.SetMapper(textMapper)
    textActor.SetScale(0.1, 0.1, 0.1)  # 1/10th of the length
    textActor.AddPosition(midpoint[0], midpoint[1], midpoint[2])
    textActor.GetProperty().SetColor(color)

    return textActor


def temp_length_calc_function(length_array):
    return round(length_array[2], 2)