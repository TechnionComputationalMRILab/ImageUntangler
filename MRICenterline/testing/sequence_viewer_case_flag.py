#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scrub through the sequence viewer and get the case flag, see if it changes and if so, how many times
a changing case flag means that there's something wrong with how the slice index is calculated
"""

import os
from PyQt5 import QtCore
from PyQt5.Qt import *
import pytest

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget

PATH_FOR_TEST_CASES = r'C:\Users\ang.a\Database\Rambam\cleaner_cases'
cases = [os.path.join(PATH_FOR_TEST_CASES, name)
         for name in os.listdir(PATH_FOR_TEST_CASES)
         if os.path.isdir(os.path.join(PATH_FOR_TEST_CASES, name))]


@pytest.mark.parametrize('folder', cases)
def test(qtbot, folder):
    case_model = CaseModel(folder)

    widget = MainDisplayWidget(case_model)
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton)
    qtbot.keyPress(widget.interactor, Qt.Key_Home)

    def assert_slice_1():
        assert case_model.sequence_viewer.slice_idx == 1

    qtbot.waitUntil(assert_slice_1)

    case_flags = []

    qtbot.keyPress(widget.interactor, Qt.Key_Up)

    while case_model.sequence_viewer.test_slice_ok:
        qtbot.keyPress(widget.interactor, Qt.Key_Up)
        case_flags.append(case_model.sequence_viewer.test_slice_idx_flag == 2)

    assert all(case_flags)
