from typing import Tuple, List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkRenderer, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D, vtkMatrix4x4, vtkCornerAnnotation

from MRICenterline.gui.help.help_text import InteractorHelpText
from MRICenterline.gui.vtk.sequence_interactor_style import SequenceViewerInteractorStyle
from MRICenterline.gui.vtk.IUCornerAnnotation import IUCornerAnnotation, CornerLoc
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

        self.test_slice_idx_flag = 0
        self.test_slice_ok = True

        self.slice_idx = self.image.sliceIdx
        self.level_val = self.image.level_value
        self.window_val = self.image.window_value

        self.window = self.interactor.GetRenderWindow()

        self.panel_actor = vtkImageActor()
        self.panel_renderer = vtkRenderer()
        self.reslice = vtkImageReslice()
        self.connect_panel_actor()

        self.cursor = vtkCursor2D()
        self.show_cursor = CFG.get_boolean('display', 'show-interactor-cursor')
        self.initialize_cursor()

        self.show_help = CFG.get_boolean('display', 'show-interactor-help')
        self.show_debug = CFG.get_boolean('display', 'show-interactor-debug')

        # initialize texts
        self.status_texts = {
            "Slice Index": self.slice_idx,
            "Window Value": self.window_val,
            "Level Value": self.level_val
        }
        self.length_texts = dict()

        self.status_text_actor = IUCornerAnnotation(CornerLoc.LOWER_LEFT)
        self.help_text_actor = IUCornerAnnotation(CornerLoc.LOWER_RIGHT)
        self.debug_text_actor = IUCornerAnnotation(CornerLoc.UPPER_RIGHT)
        self.length_text_actor = IUCornerAnnotation(CornerLoc.UPPER_LEFT)

        self.initialize_text()
        self.adjust_slice_idx(1)

        self.window.Render()

        logging.debug(f'Loading {self.slice_idx}')

    def print_status_to_terminal(self):
        logging.info(f'''
            Slice index: {self.slice_idx}
            Window value: {self.window_val}
            Level value: {self.level_val}
            Show cursor: {self.show_cursor}
        ''')

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
        cursor_actor.GetProperty().SetColor(CFG.get_color('display', 'cursor-color'))
        self.panel_renderer.AddActor(cursor_actor)

        if self.show_cursor:
            pass
        else:
            self.cursor.AllOff()

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

    def initialize_text(self):
        self.status_text_actor.SetInput(self.status_texts)
        self.status_text_actor.SetColor(CFG.get_color('display', 'text-color'))

        self.length_text_actor.SetInput(self.length_texts)
        self.length_text_actor.SetColor(CFG.get_color('display', 'text-color'))

        self.help_text_actor.SetInput(InteractorHelpText.text_out)
        self.help_text_actor.SetColor(CFG.get_color('display', 'help-text-color'))

        self.debug_text_actor.SetInput(" ")
        self.debug_text_actor.SetColor(CFG.get_color('display', 'debug-text-color'))

        self.help_text_actor.SetVisibility(self.show_help)
        self.debug_text_actor.SetVisibility(self.show_debug)

        self.panel_renderer.AddViewProp(self.status_text_actor)
        self.panel_renderer.AddViewProp(self.length_text_actor)
        self.panel_renderer.AddViewProp(self.help_text_actor)
        self.panel_renderer.AddViewProp(self.debug_text_actor)

    def update_length_text(self, val):
        self.length_texts = val
        self.length_text_actor.SetInput(self.length_texts)

    def update_status_text(self, key, val):
        self.status_texts[key] = val
        self.status_text_actor.SetInput(self.status_texts)

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
            if CFG.get_testing_status("use-slice-location"):
                z_coords = self.image.z_coords
                z = z_coords[self.slice_idx]

                if CFG.get_boolean('display', 'show-interactor-coords'):
                    self.update_status_text("Coordinates", f'x: {round(coords[0], 2)}, y: {round(coords[1], 2)}, z: {round(z, 2)}')

            else:
                if CFG.get_boolean('display', 'show-interactor-coords'):
                    self.update_status_text("Coordinates", f'x: {round(coords[0], 2)}, y: {round(coords[1], 2)}')
        except TypeError:  # it's out of bounds
            pass
        self.window.Render()

    def update_debug_text(self, text):
        self.debug_text_actor.SetInput(text)

    ###########################################################################
    #                              panel actors                               #
    ###########################################################################

    def connect_panel_actor(self):
        self.reslice.SetInputData(self.image.vtk_data)
        self.reslice.SetOutputDimensionality(2)
        self.reslice.SetResliceAxes(self.image.transformation)
        # self.reslice.SetInterpolationModeToLinear()
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
        logging.debug(f"DEBUG Case Flag: {self.test_slice_idx_flag}")

        self.window.Render()

    ######################################################################
    #                          callback functions                        #
    ######################################################################

    def adjust_window(self, window: int):
        self.panel_actor.GetProperty().SetColorWindow(window)
        self.window_val = window
        self.update_status_text("Window Value", int(self.window_val))
        self.window.Render()

    def adjust_level(self, level: int):
        self.panel_actor.GetProperty().SetColorLevel(level)
        self.level_val = level
        self.update_status_text("Level Value", int(self.level_val))
        self.window.Render()

    def update_window_level(self):
        self.level_val = self.panel_actor.GetProperty().GetColorLevel()
        self.window_val = self.panel_actor.GetProperty().GetColorWindow()
        self.update_status_text("Level Value", int(self.level_val))
        self.update_status_text("Window Value", int(self.window_val))
        self.window.Render()

        return self.window_val, self.level_val

    def update_zoom_factor(self):
        current_scale = self.panel_renderer.GetActiveCamera().GetParallelScale()
        new_zoom_factor = current_scale / self.image.get_parallel_scale()
        self.panel_renderer.GetActiveCamera().SetParallelScale(self.image.get_parallel_scale() * new_zoom_factor)
        self.window.Render()

    def go_to_first_slice_index(self, reverse: bool = False):
        """ Mainly used for testing. Forces the viewer to go to the first slice (or last, if reverse=True)"""
        if reverse:
            while self.slice_idx < self.image.size[2]-1:
                self.adjust_slice_idx(1)
        else:
            while self.slice_idx > 1:
                self.adjust_slice_idx(-1)

    def jump_to_index(self, move_to: int):
        self.adjust_slice_idx(move_to - self.slice_idx)

    def adjust_slice_idx(self, delta: int):
        import numpy as np

        # self.reslice.Update()
        spacing = self.reslice.GetOutput().GetSpacing()[2]
        matrix: vtkMatrix4x4 = self.reslice.GetResliceAxes()

        center = [round(i, 1) for i in matrix.MultiplyPoint((0, 0, delta * spacing, 1))]
        if CFG.get_testing_status("use-slice-location"):
            # center = [round(i, 1) for i in matrix.MultiplyPoint((0, 0, delta * spacing, 1))]
            slice_idx = 1 + np.int(np.round(((center[2] - self.image.origin[2]) / self.image.spacing[2])))
        else:
            # center = matrix.MultiplyPoint((0, 0, delta * spacing, 1))
            slice_idx = 1 + np.int(np.round(((center[2] - self.image.origin[2]) / self.image.spacing[2])))

        if 1 <= slice_idx <= self.image.size[2]:
            matrix = self.reslice.GetResliceAxes()
            matrix.SetElement(0, 3, center[0])
            matrix.SetElement(1, 3, center[1])
            matrix.SetElement(2, 3, center[2])

            if slice_idx == self.slice_idx:
                self.slice_idx = slice_idx + delta
                self.image.sliceIdx = slice_idx + delta
                length_count, mpr_count = self.display_points_in_slice(slice_idx + delta)
                self.test_slice_idx_flag = 1
            else:
                self.slice_idx = slice_idx
                self.image.sliceIdx = slice_idx
                length_count, mpr_count = self.display_points_in_slice(slice_idx)
                self.test_slice_idx_flag = 2

            self.update_status_text("Slice Index", self.slice_idx)
            self.render_panel()

            self.reslice.Update()
            self.update_debug_text(f"L {length_count} | M {mpr_count}"
                                   f"\n case_flag {self.test_slice_idx_flag}"
                                   f"\n center {center}")

            self.test_slice_ok = True
        else:
            # slicing failed
            self.test_slice_ok = False

    ######################################################################
    #                       point-related functions                      #
    ######################################################################

    def add_actor(self, actor):
        self.panel_renderer.AddActor(actor)
        self.render_panel()

    def display_points_in_slice(self, slice_index):
        length_count = self.model.length_point_array.show_for_slice(slice_index)
        mpr_count = self.model.mpr_point_array.show_for_slice(slice_index)
        return length_count, mpr_count
