import os
from PyQt5 import QtCore

from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.gui.display.main_widget import MainDisplayWidget

PATH_FOR_TEST_CASES = r'C:\Users\ang.a\Database\Rambam\clean_cases_test'


def test(qtbot):
    cases = [os.path.join(PATH_FOR_TEST_CASES, name)
             for name in os.listdir(PATH_FOR_TEST_CASES)
             if os.path.isdir(os.path.join(PATH_FOR_TEST_CASES, name))]

    case_model = CaseModel(cases[0])
    widget = MainDisplayWidget(case_model)
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.interactor, QtCore.Qt.LeftButton)

    assert case_model.path == cases[0]
