import vtkmodules.all as vtk

from MRICenterline.gui.vtk.widget import IUVTKWidget
from MRICenterline.app.config.internal_config import BG_COLOR


class CaseWidget(IUVTKWidget):
    def __init__(self, model, interactor, interactor_style, parent_widget=None):
        self.reslice = vtk.vtkImageReslice()
        super().__init__(model, interactor, interactor_style, parent_widget)

    def configure_actor(self):
        # # Extract a slice in the desired orientation
        self.reslice.SetInputData(self.model.image_properties.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(self.model.image_properties.transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

        # # # Create a greyscale lookup table
        table = vtk.vtkLookupTable()
        table.SetRange(0, 1000)  # image intensity range
        table.SetValueRange(0.0, 1.0)  # from black to white
        table.SetSaturationRange(0.0, 0.0)  # no color saturation
        table.SetRampToLinear()
        table.Build()

        # # Map the image through the lookup table
        color = vtk.vtkImageMapToColors()
        color.SetLookupTable(table)
        color.SetInputData(self.reslice.GetOutput())

        # set up renderer
        self.ren.SetBackground(BG_COLOR[0], BG_COLOR[1], BG_COLOR[2])
        self.ren.SetLayer(0)

        # connect to actor
        self.actor.GetMapper().SetInputConnection(color.GetOutputPort())

    def configure_camera(self):
        self.ren.GetActiveCamera().ParallelProjectionOn()
        self.ren.ResetCamera()
        self.ren.GetActiveCamera().SetParallelScale(self.model.image_properties.get_parallel_scale())
