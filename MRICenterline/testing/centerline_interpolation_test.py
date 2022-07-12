#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
checks if the centerline calculation results in an interpolation error
"""

import pytest
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from vtkmodules.all import vtkOutputWindow

from MRICenterline.app.database import name_id
from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.app.gui_data_handling.centerline_model import CenterlineModel
from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.gui.centerline.widget import CenterlineWidget
from MRICenterline.gui.display.main_widget import MainDisplayWidget

from MRICenterline.testing.test_utils import generate_list_of_sessions

session_data = generate_list_of_sessions()

# TESTING = "angle"
TESTING = "height"

@pytest.mark.parametrize('session', session_data)
def test(qtbot, session):
# def test(qtbot, session=session_data[47]):  # test one case
    # load the case from the session ID
    session_id, case_path = session

    seq_id, case_id, lengths_id, cl_id = name_id.from_session_id(session_id)
    seq_name = name_id.get_sequence_name(seq_id, case_id)

    case_model = CaseModel(case_path, seq_name)
    centerline_model = CenterlineModel(case_model)
    case_model.set_centerline_model(centerline_model)

    main_display_widget = MainDisplayWidget(case_model)
    centerline_widget = CenterlineWidget(centerline_model)
    centerline_model.connect_widget(centerline_widget)

    # turn on the interactor
    qtbot.addWidget(main_display_widget)
    qtbot.mouseClick(main_display_widget.interactor, QtCore.Qt.LeftButton)

    qtbot.addWidget(centerline_widget)
    qtbot.mouseClick(centerline_widget.interactor, QtCore.Qt.LeftButton)

    case_model.load_points(lengths_id, cl_id)

    mpr_points = len(case_model.sequence_manager.mpr_point_array)

    print(f'Calculating over {mpr_points} points')
    print(f"Seq/Case: {seq_id, case_id}")
    print(f"Orientation: {case_model.sequence_manager.orientation}")

    if mpr_points:
        # click calculate centerline
        case_model.calculate(PointStatus.MPR)

        if TESTING == "angle":
            # change the angle by a full cycle
            for i in range(0, 180):
                case_model.centerline_model.adjust_angle(1)

        if TESTING == "height":
            # change the height by 10
            for i in range(0, 100):
                case_model.centerline_model.adjust_height(1)
    else:
        print("Skipping")
