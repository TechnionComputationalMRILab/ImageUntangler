from vtkmodules.all import vtkMatrix4x4


def transformation_matrix(center, view='axial'):
    """
    Matrices for axial, coronal, sagittal orientations
    """
    matrix = vtkMatrix4x4()

    if view == 'coronal':
        matrix.DeepCopy((1, 0, 0, center[0],
                          0, 0, 1, center[1],
                          0,-1, 0, center[2],
                          0, 0, 0, 1))
    elif view == 'sagittal':
        matrix.DeepCopy((0, 0,-1, center[0],
                           1, 0, 0, center[1],
                           0,-1, 0, center[2],
                           0, 0, 0, 1))
    elif view == 'axial':
        matrix.DeepCopy((1, 0, 0, center[0],
                         0, 1, 0, center[1],
                         0, 0, 1, center[2],
                         0, 0, 0, 1))
    elif view == 'y_flip_axial':
        matrix.DeepCopy((1, 0, 0, center[0],
                         0, -1, 0, center[1],
                         0, 0, 1, center[2],
                         0, 0, 0, 1))
    else:  # same as axial
        matrix.DeepCopy((1, 0, 0, center[0],
                         0, 1, 0, center[1],
                         0, 0, 1, center[2],
                         0, 0, 0, 1))

    return matrix
