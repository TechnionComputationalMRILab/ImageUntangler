from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkRenderer, vtkTextActor

from MRICenterline.gui.vtk.IUCornerAnnotation import IUCornerAnnotation, CornerLoc
from MRICenterline.gui.vtk.text_actor import IUTextActor
from MRICenterline.gui.vtk.sequence_interactor_style import SequenceViewerInteractorStyle
from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class CenterlineViewer:
    def __init__(self,
                 model,
                 interactor: QVTKRenderWindowInteractor,
                 interactor_style: SequenceViewerInteractorStyle):
        self.model = model
        self.interactor = interactor
        self.interactor_style = interactor_style

        self.window = self.interactor.GetRenderWindow()

        self.reslice = vtkImageReslice()
        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()

        self.height_text_actor = IUTextActor("Height: " + str(self.model.height), True, 0)
        self.angle_text_actor = IUTextActor("Angle: " + str(self.model.angle), True, 1)

    def set_window_level(self):
        self.panel_actor.GetProperty().SetColorWindow(self.model.window_value)
        self.panel_actor.GetProperty().SetColorLevel(self.model.level_value)
        self.window.Render()

    def connect_panel_actor(self):
        self.reslice.SetInputData(self.model.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.Update()

        self.panel_actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())

        self.panel_renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.panel_renderer.AddActor(self.panel_actor)
        self.panel_renderer.SetLayer(0)

        self.window.AddRenderer(self.panel_renderer)
        self.interactor_style.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactor_style)
        self.window.SetInteractor(self.interactor)

        self.panel_renderer.GetActiveCamera().ParallelProjectionOn()
        self.panel_renderer.ResetCamera()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.model.parallel_scale)

    def initialize_panel(self):
        self.set_window_level()
        self.connect_panel_actor()

        self.panel_renderer.AddActor(self.height_text_actor)
        self.panel_renderer.AddActor(self.angle_text_actor)

        self.reslice.Update()
        self.window.Render()

    def add_actor(self, actor):
        self.panel_renderer.AddActor(actor)
        self.refresh_panel()

    def refresh_panel(self, angle_change=None, height_change=None):
        logging.debug(f"Current number of actors: {self.panel_renderer.GetActors().GetNumberOfItems()}")
        self.reslice.SetInputData(self.model.vtk_data)
        self.reslice.Update()

        if angle_change:
            self.angle_text_actor.SetInput("Angle: " + str(self.model.angle))
        if height_change:
            self.height_text_actor.SetInput("Height: " + str(self.model.height))

        self.window.Render()
