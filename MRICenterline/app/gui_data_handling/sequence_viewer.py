from typing import List
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkImageActor, vtkImageReslice, vtkRenderer, vtkTextActor, vtkPolyDataMapper,\
    vtkActor, vtkCursor2D, vtkMatrix4x4

from MRICenterline.gui.vtk.interactor_style import SequenceViewerInteractorStyle
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline import CFG, CONST

import logging
logging.getLogger(__name__)


class SequenceViewer:
    panel_actor = vtkImageActor()
    panel_renderer = vtkRenderer()
    reslice = vtkImageReslice()
    cursor = vtkCursor2D()
    
    def __init__(self, 
                 viewer_manger,
                 image_properties: ImageProperties,  
                 interactor: QVTKRenderWindowInteractor,
                 interactor_style: SequenceViewerInteractorStyle):
        self.manager = viewer_manger
        self.interactor = interactor
        self.interactor_style = interactor_style
        self.image = image_properties
        self.window = self.interactor.GetRenderWindow()

        self.slice_idx = self.image.sliceIdx
        self.pastIndex = self.slice_idx
        self.level_val = self.image.level_value
        self.window_val = self.image.window_value

        self.initialize_text_actors()
        self.connect_panel_actor()

        self.window.Render()
        
    def initialize_text_actors(self):
        pass
    
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
        # self.textActorWindow.SetInput("Window: " + str(np.int32(self.window_val)))
        self.window.Render()

    def adjust_level(self, level: int):
        self.panel_actor.GetProperty().SetColorLevel(level)
        self.level_val = level
        # self.textActorLevel.SetInput("Level: " + str(np.int32(self.level_val)))
        self.window.Render()

    def update_window_level(self):
        self.manager.change_window(self.panel_actor.GetProperty().GetColorWindow())
        self.manager.change_level(self.panel_actor.GetProperty().GetColorLevel())

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
        slice_idx = np.int(1 + (np.round(((center[2] - self.image.origin[2]) / self.image.spacing[2]))))

        if 1 <= slice_idx <= self.image.size[2]:
            matrix = self.reslice.GetResliceAxes()
            matrix.SetElement(0, 3, center[0])
            matrix.SetElement(1, 3, center[1])
            matrix.SetElement(2, 3, center[2])
            # self.textActorSliceIdx.SetInput("SliceIdx: " + str(1 + self.imageData.size[2] - slice_idx))

            self.slice_idx = slice_idx
            self.image.sliceIdx = slice_idx
            # self.manager.update_slider_index(self.slice_idx)
            self.display_points_in_slice(slice_idx)
            self.render_panel()

    ######################################################################
    #                       point-related functions                      #
    ######################################################################

    def add_point_actor(self, point_actor):
        self.panel_renderer.AddActor(point_actor)
        self.render_panel()

    def display_points_in_slice(self, slice_index):
        self.manager.model.length_point_array.show_points_for_slice(slice_index)
        self.manager.model.mpr_point_array.show_points_for_slice(slice_index)
