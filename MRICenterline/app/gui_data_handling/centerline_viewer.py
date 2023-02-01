from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkRenderer, vtkActor2D, vtkTextMapper, vtkTextProperty

from MRICenterline.gui.help.help_text import CenterlineInteractorHelpText
from MRICenterline.gui.vtk.IUCornerAnnotation import CornerLoc, IUCornerAnnotation
from MRICenterline.gui.vtk.centerline_interactor_style import CenterlineInteractorStyle

from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class CenterlineViewer:
    def __init__(self,
                 model,
                 interactor: QVTKRenderWindowInteractor,
                 interactor_style: CenterlineInteractorStyle):
        self.model = model
        self.interactor = interactor
        self.interactor_style = interactor_style

        self.window = self.interactor.GetRenderWindow()

        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()
        self.removable_actor_list = []

        self.status_texts = {
            "Height": self.model.height,
            "Angle": self.model.angle,
        }
        self.status_text_actor = IUCornerAnnotation(CornerLoc.LOWER_LEFT)
        self.help_text_actor = IUCornerAnnotation(CornerLoc.LOWER_RIGHT)

        self.initialize_text()

    def initialize_text(self):
        self.status_text_actor.SetInput(self.status_texts)
        self.status_text_actor.SetColor(CFG.get_color('display', 'text-color'))

        self.help_text_actor.SetInput(CenterlineInteractorHelpText.text_out)
        self.help_text_actor.SetColor(CFG.get_color('display', 'help-text-color'))

        self.panel_renderer.AddViewProp(self.status_text_actor)
        self.panel_renderer.AddViewProp(self.help_text_actor)

    def set_window_level(self):
        self.panel_actor.GetProperty().SetColorWindow(self.model.window_value)
        self.panel_actor.GetProperty().SetColorLevel(self.model.level_value)
        self.window.Render()

    def connect_panel_actor(self):
        self.panel_actor.GetMapper().SetInputData(self.model.vtk_data)

        self.panel_renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.panel_renderer.AddActor(self.panel_actor)
        self.panel_renderer.SetLayer(0)

        self.window.AddRenderer(self.panel_renderer)
        self.interactor_style.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactor_style)
        self.window.SetInteractor(self.interactor)

        self.panel_renderer.GetActiveCamera().ParallelProjectionOn()
        self.panel_renderer.ResetCamera()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.model.parallel_scale*0.1)

        for line in self.model.point_markers:
            self.panel_renderer.AddActor(line)

    def initialize_panel(self):
        self.connect_panel_actor()
        self.set_window_level()
        self.window.Render()

    def add_actor(self, actor):
        self.removable_actor_list.append(actor)
        self.panel_renderer.AddActor(actor)
        self.refresh_panel()

    def add_actor_annotation(self, x, y, pt_num):
        text_property = vtkTextProperty()
        text_property.SetFontSize(30)
        text_property.SetJustificationToCentered()
        text_property.SetColor(0, 0, 1)

        text_mappers = vtkTextMapper()
        text_mappers.SetInput(str(pt_num))
        text_mappers.SetTextProperty(text_property)

        text_actor = vtkActor2D()
        text_actor.SetMapper(text_mappers)
        text_actor.SetPosition(x, y)

        self.removable_actor_list.append(text_actor)
        self.panel_renderer.AddActor(text_actor)
        self.refresh_panel()

    def refresh_panel(self, angle_change=None, height_change=None):
        logging.debug(f"Current number of actors: {self.panel_renderer.GetActors().GetNumberOfItems()}")
        self.panel_actor.GetMapper().SetInputData(self.model.vtk_data)

        if angle_change:
            self.update_status_text("Angle", str(self.model.angle))
        if height_change:
            self.update_status_text("Height", str(self.model.height))

        self.window.Render()

    def update_status_text(self, key, val):
        self.status_texts[key] = val
        self.status_text_actor.SetInput(self.status_texts)

    def clear_removable_actors(self):
        for actor in self.removable_actor_list:
            self.panel_renderer.RemoveActor(actor)
        self.refresh_panel()

    def highlight_line_marker(self, index):
        self.model.point_markers[index].change_color(CFG.get_color('mpr-length-display-style', 'highlighted-color'))
        self.window.Render()
