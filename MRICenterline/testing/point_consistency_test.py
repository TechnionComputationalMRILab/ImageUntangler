#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
clicks random points on the interactor, loads them, and checks if the points are loaded
on the same slice indices
"""
from copy import deepcopy

import pytest
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from vtkmodules.all import vtkOutputWindow

from MRICenterline.app.database import name_id
from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.app.points.status import PickerStatus
from MRICenterline.gui.display.main_widget import MainDisplayWidget

from MRICenterline.testing.test_utils import generate_file_list

cases = generate_file_list()


@pytest.mark.parametrize('folder', cases)
def test(qtbot, folder):
# def test(qtbot, folder=cases[47]):  # test one case
    # move VTK warnings/errors to terminal
    vtk_out = vtkOutputWindow()
    vtk_out.SetDisplayMode(0)

    # initialize model
    case_model = CaseModel(folder)

    widget = MainDisplayWidget(case_model)
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton)

    # initial pick points
    case_model.set_picker_status(PickerStatus.PICKING_MPR)

    dots_per_slice = 25

    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Up, modifier=QtCore.Qt.NoModifier, delay=50)

    for x, y in zip(np.linspace(55, 50, dots_per_slice), np.linspace(15, 20, dots_per_slice)):
        qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(x, y),
                         modifier=QtCore.Qt.NoModifier, delay=50)

    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Up, modifier=QtCore.Qt.NoModifier, delay=50)

    for x, y in zip(np.linspace(50, 45, dots_per_slice), np.linspace(20, 15, dots_per_slice)):
        qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(x, y),
                         modifier=QtCore.Qt.NoModifier, delay=50)

    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Up, modifier=QtCore.Qt.NoModifier, delay=50)

    for x, y in zip(np.linspace(45, 50, dots_per_slice), np.linspace(15, 10, dots_per_slice)):
        qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(x, y),
                         modifier=QtCore.Qt.NoModifier, delay=50)

    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Down, modifier=QtCore.Qt.NoModifier, delay=50)

    for x, y in zip(np.linspace(50, 55, dots_per_slice), np.linspace(10, 15, dots_per_slice)):
        qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(x, y),
                         modifier=QtCore.Qt.NoModifier, delay=50)

    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Down, modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(50, 15),
                     modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Down, modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(50, 15),
                     modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Down, modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(50, 15),
                     modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.keyPress(widget.interactor, QtCore.Qt.Key_Down, modifier=QtCore.Qt.NoModifier, delay=50)
    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton, pos=QPoint(50, 15),
                     modifier=QtCore.Qt.NoModifier, delay=50)

    mpr_point_array = case_model.sequence_manager.mpr_point_array

    # make sure that all the points made are valid
    for pt in mpr_point_array:
        for index in pt.itk_index_coords:
            assert index >= 0

    # assert len(mpr_point_array) == 100

    saved_points = deepcopy(mpr_point_array.simplify())
    saved_slices_with_points = deepcopy(mpr_point_array.get_slices_with_points())
    saved_session_id = case_model.save()

    # get a new case model and main widget to load everything to
    new_case_model = CaseModel(folder)

    new_widget = MainDisplayWidget(new_case_model)
    qtbot.addWidget(new_widget)
    qtbot.mouseClick(new_widget.interactor, QtCore.Qt.LeftButton)

    # load points
    seq_id, case_id, lengths_id, cl_id = name_id.from_session_id(saved_session_id)

    new_case_model.load_points(lengths_id, cl_id)

    loaded_point_array = new_case_model.sequence_manager.mpr_point_array
    loaded_points = loaded_point_array.simplify()
    loaded_slices_with_points = new_case_model.sequence_manager.mpr_point_array.get_slices_with_points()

    slice_index_comparison = []
    image_coords_comparison = []
    # slice_with_points_comparison = []

    for saved_pt, loaded_pt in zip(saved_points, loaded_points):
        # make sure that the z appear in the same slices
        slice_index_comparison.append(saved_pt['slice_index'] == loaded_pt['slice_index'])

        # only checks the x-y location. since image_coords are calculated as ints, only the integer values are compared
        saved_x = round(saved_pt['image_coords'][0])
        saved_y = round(saved_pt['image_coords'][1])

        loaded_x = round(loaded_pt['image_coords'][0])
        loaded_y = round(loaded_pt['image_coords'][1])

        comp_x = abs(saved_x - loaded_x) <= 1
        comp_y = abs(saved_y - loaded_y) <= 1

        image_coords_comparison.append(comp_x and comp_y)

        print(saved_x, saved_y, loaded_x, loaded_y)

    print(f'slice: {slice_index_comparison}')
    print(f'index: {image_coords_comparison}')

    assert all(slice_index_comparison)
    assert all(image_coords_comparison)

    # for saved_slice, loaded_slice in zip(saved_slices_with_points, loaded_slices_with_points):
    #     assert saved_slice == loaded_slice
