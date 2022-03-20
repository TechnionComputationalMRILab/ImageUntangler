from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D, vtkMatrix4x4

from MRICenterline.gui.help.help_text import InteractorHelpText
from MRICenterline.gui.vtk.interactor_style import SequenceViewerInteractorStyle
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class SequenceViewer:
    def __init__(self, 
                 viewer_manger,
                 image_properties: ImageProperties,  
                 interactor: QVTKRenderWindowInteractor,
                 interactor_style: SequenceViewerInteractorStyle):
        self.model = viewer_manger
        self.interactor = interactor
        self.interactor_style = interactor_style
        self.image = image_properties

        self.slice_idx = self.image.sliceIdx
        self.level_val = self.image.level_value
        self.window_val = self.image.window_value

        self.window = self.interactor.GetRenderWindow()

        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()
        self.reslice = vtkImageReslice()
        self.connect_panel_actor()

        self.cursor = vtkCursor2D()
        self.show_cursor = True
        self.initialize_cursor()

        self.index_text_actor = vtkTextActor()
        self.window_text_actor = vtkTextActor()
        self.level_text_actor = vtkTextActor()
        self.coords_text_actor = vtkTextActor()
        self.help_text_actor = vtkTextActor()
        self.debug_text_actor = vtkTextActor()
        self.show_help, self.show_debug = True, False
        self.initialize_text_actors()

        self.window.Render()
        
    ###########################################################################
    #                            cursor functions                             #
    ###########################################################################

    def initialize_cursor(self):
        self.cursor.SetModelBounds(-10000, 10000, -10000, 10000, 0, 0)
        self.cursor.SetFocalPoint(0, 0, 0)
        self.cursor.AxesOn()
        self.cursor.TranslationModeOn()
        self.cursor.OutlineOff()

        cursor_mapper = vtkPolyDataMapper()
        cursor_mapper.SetInputConnection(self.cursor.GetOutputPort())

        cursor_actor = vtkActor()
        cursor_actor.SetMapper(cursor_mapper)
        cursor_actor.GetProperty().SetColor(1, 0, 0)
        self.panel_renderer.AddActor(cursor_actor)

    def update_cursor_location(self, coords):
        self.cursor.SetFocalPoint(coords[0], coords[1], 0)

    def toggle_cursor(self):
        if self.show_cursor:
            self.show_cursor = False
            self.cursor.AllOff()
            self.window.Render()
        else:
            self.show_cursor = True
            self.cursor.AllOff()
            self.cursor.AxesOn()
            self.window.Render()

    ###########################################################################
    #                               text actors                               #
    ###########################################################################

    def initialize_text_actors(self):
        color = CFG.get_color('display', 'text-color')

        slice_index_loc = 0
        self.index_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.index_text_actor.GetTextProperty().SetColor(color[0], color[1], color[2])
        self.index_text_actor.SetDisplayPosition(0, slice_index_loc*int(CFG.get_config_data('display', 'font-size')))
        self.index_text_actor.SetInput("SliceIdx: " + str(self.slice_idx))
        self.panel_renderer.AddActor(self.index_text_actor)

        window_loc = 1
        self.window_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.window_text_actor.GetTextProperty().SetColor(color[0], color[1], color[2])
        self.window_text_actor.SetDisplayPosition(0, window_loc*int(CFG.get_config_data('display', 'font-size')))
        self.window_text_actor.SetInput("Window: " + str(self.window_val))
        self.panel_renderer.AddActor(self.window_text_actor)

        level_loc = 2
        self.level_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.level_text_actor.GetTextProperty().SetColor(color[0], color[1], color[2])
        self.level_text_actor.SetDisplayPosition(0, level_loc*int(CFG.get_config_data('display', 'font-size')))
        self.level_text_actor.SetInput("Level: " + str(self.level_val))
        self.panel_renderer.AddActor(self.level_text_actor)

        coords_loc = 3
        self.coords_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.coords_text_actor.GetTextProperty().SetColor(color[0], color[1], color[2])
        self.coords_text_actor.SetInput(" ")
        self.coords_text_actor.SetDisplayPosition(0, coords_loc*int(CFG.get_config_data('display', 'font-size')))
        self.panel_renderer.AddActor(self.coords_text_actor)

        help_loc = InteractorHelpText.text_length + 1
        self.help_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.help_text_actor.GetTextProperty().SetColor(*InteractorHelpText.text_color)
        self.help_text_actor.SetInput(InteractorHelpText.text_out)
        self.help_text_actor.SetDisplayPosition(0, help_loc*int(CFG.get_config_data('display', 'font-size')))
        self.help_text_actor.SetVisibility(self.show_help)
        self.panel_renderer.AddActor(self.help_text_actor)

        debug_loc = help_loc + 5
        self.debug_text_actor.GetTextProperty().SetFontSize(int(CFG.get_config_data('display', 'font-size')))
        self.debug_text_actor.GetTextProperty().SetColor(1, 0, 0)
        self.debug_text_actor.SetInput("DEBUG TEXT HERE")
        self.debug_text_actor.SetDisplayPosition(0, debug_loc*int(CFG.get_config_data('display', 'font-size')))
        self.debug_text_actor.SetVisibility(self.show_debug)
        self.panel_renderer.AddActor(self.debug_text_actor)

    def toggle_help(self):
        self.help_text_actor.SetVisibility(self.show_help)
        if self.show_help:
            self.show_help = False
        else:
            self.show_help = True

    def toggle_debug(self):
        self.debug_text_actor.SetVisibility(self.show_debug)
        if self.show_debug:
            self.show_debug = False
        else:
            self.show_debug = True

    def update_displayed_coords(self, coords):
        try:
            self.coords_text_actor.SetInput(f'x: {round(coords[0], 2)}, y: {round(coords[1], 2)}, z: {round(coords[2], 2)}')
        except TypeError:  # it's out of bounds
            pass
        self.window.Render()

    ###########################################################################
    #                              panel actors                               #
    ###########################################################################

    def connect_panel_actor(self):
        self.reslice.SetInputData(self.image.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(self.image.transformation)
        self.reslice.SetInterpolationModeToLinear()
        self.reslice.Update()

        self.panel_actor.GetMapper().SetInputConnection(self.reslice.GetOutputPort())
        self.panel_actor.GetProperty().SetColorWindow(self.window_val)
        self.panel_actor.GetProperty().SetColorLevel(self.level_val)

        self.panel_renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.panel_renderer.AddActor(self.panel_actor)
        self.panel_renderer.SetLayer(0)

        self.window.AddRenderer(self.panel_renderer)
        self.interactor_style.SetInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactor_style)
        self.window.SetInteractor(self.interactor)
        self.panel_renderer.GetActiveCamera().ParallelProjectionOn()
        self.panel_renderer.ResetCamera()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.image.get_parallel_scale())

    def render_panel(self):
        logging.debug(f"Rendering slice: {self.slice_idx} / ITK zindex: {1 + self.image.size[2] - self.slice_idx}")
        logging.debug(f"Current number of actors: {self.panel_renderer.GetActors().GetNumberOfItems()}")

        self.window.Render()

    ######################################################################
    #                          callback functions                        #
    ######################################################################

    def adjust_window(self, window: int):
        self.panel_actor.GetProperty().SetColorWindow(window)
        self.window_val = window
        self.window_text_actor.SetInput("Window: " + str(int(self.window_val)))
        self.window.Render()

    def adjust_level(self, level: int):
        self.panel_actor.GetProperty().SetColorLevel(level)
        self.level_val = level
        self.level_text_actor.SetInput("Level: " + str(int(self.level_val)))
        self.window.Render()

    def update_window_level(self):
        self.model.change_window(self.panel_actor.GetProperty().GetColorWindow())
        self.model.change_level(self.panel_actor.GetProperty().GetColorLevel())

    def update_zoom_factor(self):
        current_scale = self.panel_renderer.GetActiveCamera().GetParallelScale()
        new_zoom_factor = current_scale / self.image.get_parallel_scale()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.image.get_parallel_scale() * new_zoom_factor)
        self.window.Render()

    def adjust_slice_idx(self, delta: int):
        import numpy as np

        self.reslice.Update()
        spacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, delta*spacing, 1))

        # sliceIdx = np.int(np.round((center[2] - self.imageData.origin[2]) / self.imageData.spacing[2] - 0.5))
        slice_idx = 1 + np.int(np.round(((center[2] - self.image.origin[2]) / self.image.spacing[2])))

        if 1 <= slice_idx <= self.image.size[2]:
            matrix = self.reslice.GetResliceAxes()
            matrix.SetElement(0, 3, center[0])
            matrix.SetElement(1, 3, center[1])
            matrix.SetElement(2, 3, center[2])

            if slice_idx == self.slice_idx:
                # sometimes the calculated slice index is the same as the previous one? # TODO
                self.slice_idx = slice_idx + delta
                self.image.sliceIdx = slice_idx + delta
                self.display_points_in_slice(slice_idx + delta)
            else:
                self.slice_idx = slice_idx
                self.image.sliceIdx = slice_idx
                self.display_points_in_slice(slice_idx)

            self.index_text_actor.SetInput("SliceIdx: " + str(1 + self.image.size[2] - self.slice_idx))
            self.render_panel()

    ######################################################################
    #                       point-related functions                      #
    ######################################################################

    def add_actor(self, actor):
        self.panel_renderer.AddActor(actor)
        self.render_panel()

    def display_points_in_slice(self, slice_index):
        self.model.length_point_array.show_points_for_slice(slice_index)
        self.model.mpr_point_array.show_points_for_slice(slice_index)
