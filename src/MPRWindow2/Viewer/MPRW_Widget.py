from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from MPRWindow2.Control.MPRW_Control import MPRW_Control
from MPRWindow2.Model.MPRW_Model import MPRW_Model
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'util')))
from util import config_data, stylesheets


class MPRW_Widget(QWidget):
    def __init__(self, input_data: MPRW_Control):
        super().__init__()
        # self.model = input_model

        self._top_layout = QHBoxLayout(self)

        self._top_layout.addWidget(TestVTKinQFrame().frame, stretch=85)
        self._top_layout.addWidget(MPRWindowBottom(), stretch=15)

        self.setLayout(self._top_layout)


class MPRWindowBottom(QWidget):
    def __init__(self):
        super().__init__()
        _bottom_layout = QVBoxLayout(self)

        _bottom_layout.addWidget(HeightAngleSetter())
        _bottom_layout.addWidget(LengthCalculator())
        _bottom_layout.addWidget(LengthResultBox())


class HeightAngleSetter(QWidget):
    def __init__(self):
        super().__init__()

        _size_set_groupbox = QGroupBox(self)
        _size_set_groupbox.setFlat(True)
        _size_set_groupbox.setTitle("Set height/angle")
        self.settingsBoxLayout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        self.settingsBoxLayout.addWidget(_height_label)
        self.heightSetter = QDoubleSpinBox(_size_set_groupbox)
        self.heightSetter.setMaximum(5000.0)
        self.heightSetter.setProperty("value", 20.0)
        self.heightSetter.setSuffix(" mm")
        self.settingsBoxLayout.addWidget(self.heightSetter)

        # angle
        _angle_label = QLabel("Angle")
        self.settingsBoxLayout.addWidget(_angle_label)
        self.angleSetter = QSpinBox(_size_set_groupbox)
        self.angleSetter.setSuffix(" °")
        self.angleSetter.setMaximum(180)
        self.settingsBoxLayout.addWidget(self.angleSetter)

        # update button
        self.updateButton = QPushButton(_size_set_groupbox)
        self.updateButton.setText("Update")
        self.settingsBoxLayout.addWidget(self.updateButton)

        self.settingsBoxLayout.addSpacerItem(QSpacerItem(150, 10, QSizePolicy.Expanding))

class LengthCalculator(QWidget):
    def __init__(self):
        super().__init__()

        _calc_length_groupbox = QGroupBox(self)
        _calc_length_groupbox.setTitle("Length calculator")
        _calc_length_groupbox.setFlat(True)

        self.verticalLayout = QVBoxLayout(_calc_length_groupbox)

        self.setPointsButton = QPushButton(_calc_length_groupbox)
        self.setPointsButton.setText("Set points")
        self.verticalLayout.addWidget(self.setPointsButton)

        self.calcLengthButton = QPushButton(_calc_length_groupbox)
        self.calcLengthButton.setText("Calculate")
        self.verticalLayout.addWidget(self.calcLengthButton)

        self.saveButton = QPushButton(_calc_length_groupbox)
        self.saveButton.setText("Save to file")
        self.verticalLayout.addWidget(self.saveButton)


class LengthResultBox(QWidget):
    def __init__(self):
        super().__init__()

        _length_result_groupbox = QGroupBox(self)
        _length_result_groupbox.setTitle("Calculated Length")
        _length_result_groupbox.setFlat(True)

        self.lengthResultsLayout = QVBoxLayout(_length_result_groupbox)
        self.lengthResultsLabel = QLabel("textttttttttttttttttttttt")

        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        self.lengthResultsLayout.addWidget(self.lengthResultsLabel)


class TestVTKinQFrame:
    def __init__(self):
        self.frame = QFrame()

        self.vl = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setFlat(True)
        self.groupbox.setCheckable(False)
        self.vl.addWidget(self.groupbox)

        self.frame.setLayout(self.vl)

        self.vtkWidget = QVTKRenderWindowInteractor(self.groupbox)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.ren.AddActor(actor)

        self.ren.ResetCamera()

        self.iren.Initialize()
        self.iren.Start()
