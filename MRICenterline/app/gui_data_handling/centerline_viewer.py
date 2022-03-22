from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D, vtkMatrix4x4

from MRICenterline.gui.help.help_text import InteractorHelpText
from MRICenterline.gui.vtk.sequence_interactor_style import SequenceViewerInteractorStyle
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
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

    def connect_panel_actor(self):
        self.reslice.SetInputData(self.model.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.Update()

        self.panel_actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.panel_actor.GetProperty().SetColorWindow(252)
        self.panel_actor.GetProperty().SetColorLevel(126)

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

    def refresh_panel(self):
        self.connect_panel_actor()
        self.reslice.Update()
        self.window.Render()
