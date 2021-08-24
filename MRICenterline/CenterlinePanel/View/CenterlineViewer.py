import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QDoubleSpinBox, QSpinBox, QPushButton
from PyQt5.QtGui import QFont
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from typing import List

from MRICenterline.CenterlinePanel.Control.CenterlineViewerInteractorStyle import MPRInteractorStyle
from MRICenterline.Points.PointCollection import PointCollection

from MRICenterline.utils import program_constants as CONST
from MRICenterline.Config import ConfigParserRead as CFG
from MRICenterline.utils import message as MSG

import logging
logging.getLogger(__name__)


class CenterlineViewer(QWidget):
    def __init__(self, model, control, parent=None):
        super().__init__(parent=parent)
        logging.debug("Initializing panel widgets")
        self.model = model
        self.control = control
        self.lengthPoints = PointCollection()

        self.vl = QVBoxLayout(parent)
        self.setLayout(self.vl)

        self._initialize_top()
        self._initialize_bottom()

    def _initialize_top(self):
        logging.debug("Top widget of MPR Window initializing")
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vl.addWidget(self.vtkWidget)

        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.set_text_actors()
        self.actor = self.control.get_actor()
        self.renderer.AddActor(self.actor)

        self.renderer.SetBackground(CONST.BG_COLOR[0], CONST.BG_COLOR[1], CONST.BG_COLOR[2])
        self.renderer.ResetCamera()

        self.renderWindow = self.iren.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.interactorStyle = MPRInteractorStyle(parent=self.iren, MPRWindow=self, model=self.model)
        self.interactorStyle.SetInteractor(self.iren)
        self.iren.SetInteractorStyle(self.interactorStyle)
        self.renderWindow.SetInteractor(self.iren)

        self.renderWindow.Render()
        self.renderer.ResetCamera()
        self.iren.Initialize()
        self.iren.Start()
        logging.debug("Top widget of MPR Window starting")

    def updateWindowAndLevel(self):
        _window = self.actor.GetProperty().GetColorWindow()
        _level = self.actor.GetProperty().GetColorLevel()
        self.textActorWindow.SetInput("Window: " + str(np.int32(_window)))
        self.textActorLevel.SetInput("Level: " + str(np.int32(_level)))
        self.textActorAngle.SetInput("Angle: " + str(np.int32(self.model.angle)))

    def set_text_actors(self):
        logging.debug("Setting text actors")
        _font_size = int(CFG.get_config_data('display', 'font-size'))
        _display_color = CFG.get_color('display')
        _order = CONST.ORDER_OF_CONTROLS

        self.textActorLevel = vtk.vtkTextActor()
        self.textActorLevel.GetTextProperty().SetFontSize(_font_size)
        self.textActorLevel.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorLevel.SetDisplayPosition(0, _order.index('Level')*_font_size)
        self.textActorLevel.SetInput(f"Level: {self.model.interface.level}")
        self.renderer.AddActor(self.textActorLevel)

        self.textActorWindow = vtk.vtkTextActor()
        self.textActorWindow.GetTextProperty().SetFontSize(_font_size)
        self.textActorWindow.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorWindow.SetDisplayPosition(0, _order.index('Window')*_font_size)
        self.textActorWindow.SetInput(f"Window: {self.model.interface.window}")
        self.renderer.AddActor(self.textActorWindow)

        _angle_text_actor_order = _order.index('Angle') if 'Angle' in _order else _order.index('Slice Index')
        self.textActorAngle = vtk.vtkTextActor()
        self.textActorAngle.GetTextProperty().SetFontSize(_font_size)
        self.textActorAngle.GetTextProperty().SetColor(_display_color[0], _display_color[1], _display_color[2])
        self.textActorAngle.SetDisplayPosition(0, _angle_text_actor_order*_font_size)
        self.textActorAngle.SetInput("Angle: " + str(self.model.angle))
        self.renderer.AddActor(self.textActorAngle)

    def _initialize_bottom(self):
        _bottom_widget = QWidget()
        _bottom_layout = QHBoxLayout()
        _bottom_widget.setLayout(_bottom_layout)
        _bottom_layout.addWidget(self._height_angle_groupbox())
        _bottom_layout.addWidget(self._build_length_calc_box())
        _bottom_layout.addWidget(self._build_length_results_box())
        self.vl.addWidget(_bottom_widget)

    def _height_angle_groupbox(self) -> QGroupBox:
        logging.debug("First bottom widget of MPR Window initialized")
        _size_set_groupbox = QGroupBox()

        _set_height_angle_layout = QVBoxLayout(_size_set_groupbox)

        # height
        _height_label = QLabel("Height")
        _set_height_angle_layout.addWidget(_height_label)

        self._height_set_box = QDoubleSpinBox(_size_set_groupbox)
        self._height_set_box.setMinimum(CONST.CL_MIN_HEIGHT)
        self._height_set_box.setMaximum(CONST.CL_MAX_HEIGHT)
        self._height_set_box.setProperty("value", CONST.CL_INITIAL_HEIGHT)
        self._height_set_box.valueChanged.connect(self.update_height)
        self._height_set_box.setSuffix(" mm")
        _set_height_angle_layout.addWidget(self._height_set_box)

        # angle
        _angle_label = QLabel("Angle")
        _set_height_angle_layout.addWidget(_angle_label)

        self._angle_set_box = QSpinBox(_size_set_groupbox)
        self._angle_set_box.setMinimum(CONST.CL_MIN_ANGLE)
        self._angle_set_box.setMaximum(CONST.CL_MAX_ANGLE)
        self._angle_set_box.setProperty("value", CONST.CL_INITIAL_ANGLE)
        self._angle_set_box.valueChanged.connect(self.update_angle)
        self._angle_set_box.setSuffix(" °")
        _set_height_angle_layout.addWidget(self._angle_set_box)

        return _size_set_groupbox

    def update_height(self):
        _height = self._height_set_box.value()
        self.model.set_height(_height)
        logging.info(f'Height updated {_height}')

        self.actor = self.control.get_actor()
        self.renderer.AddActor(self.actor)
        self.renderWindow.Render()

    def update_angle(self, angle_change=None):
        if angle_change:
            # angle changed using mouse wheel
            self.model.change_angle(angle_change)
        else:
            # angle changed using box
            # _angle =
            self.model.set_angle(self._angle_set_box.value())

        self._angle_set_box.setValue(self.model.angle)

        self.actor = self.control.get_actor()
        self.renderer.AddActor(self.actor)
        self.renderWindow.Render()
        logging.info(f'Angle updated {self.model.angle}')

    def _build_length_calc_box(self):
        logging.debug("Second bottom widget of MPR Window initialized")
        _length_calc_groupbox = QGroupBox(self)

        _length_calc_layout = QVBoxLayout(_length_calc_groupbox)

        self._set_points_button = QPushButton("Set Points")
        _length_calc_layout.addWidget(self._set_points_button)
        self._set_points_button.clicked.connect(self.setPointsButtonClick)

        _calc_length_button = QPushButton("Calculate Length")
        _length_calc_layout.addWidget(_calc_length_button)
        _calc_length_button.clicked.connect(self.calculateDistances)

        _save_button = QPushButton("Save")
        _length_calc_layout.addWidget(_save_button)
        _save_button.clicked.connect(self._save_file)

        return _length_calc_groupbox

    def _build_length_results_box(self):
        logging.debug("Third bottom widget of MPR Window initialized")
        _length_results_group_box = QGroupBox(self)

        _length_results_layout = QVBoxLayout(_length_results_group_box)

        self._length_results_label = QLabel("Calculated Length")

        _font = QFont()
        _font.setBold(True)
        _font.setWeight(75)
        self._length_results_label.setFont(_font)

        _length_results_layout.addWidget(self._length_results_label)

        return _length_results_group_box

    def setPointsButtonClick(self):
        if self.interactorStyle.actions["Picking"] == 0:
            self.interactorStyle.actions["Picking"] = 1
            self._set_points_button.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.interactorStyle.actions["Picking"] = 0
            self._set_points_button.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

    def generateIndices(self, lengthPoints, delta) -> List[List[int]]:
        return [[int(point.image_coordinates[0] // self.model.get_mpr_properties().delta), int(point.image_coordinates[1] // delta)]
                for point in lengthPoints.points]

    def calculateDistances(self) -> None:
        # calculate and output distance of length points in MPRwindow Viewer

        if len(self.lengthPoints) >= 2:
            indices = self.generateIndices(self.lengthPoints, self.model.get_mpr_properties().delta)
            MPR_Position = self.model.get_mpr_properties().MPR_indexs_np

            pointsPositions = [MPR_Position[indices[i][0], indices[i][1], :] for i in range(len(indices))]
            pointsPositions = np.asarray(pointsPositions)
            allLengths = [np.linalg.norm(pointsPositions[j, :] - pointsPositions[j + 1, :]) for j in
                          range(len(pointsPositions) - 1)]
            totalDistance = np.sum(allLengths)
            self.outputLengthResults(totalDistance, allLengths)
        else:
            MSG.msg_box_warning("Not enough points clicked to calculate length")

    def outputLengthResults(self, total_distance, all_lengths):
        strdis = ["{0:.2f}".format(all_lengths[i]) for i in range(len(all_lengths))]
        self._length_results_label.setText("The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),"{0:.2f}".format(total_distance)))

    def processNewPoint(self, pickedCoordinates):
        coordinates = [pickedCoordinates[0], pickedCoordinates[1], pickedCoordinates[2], 0] # x,y,z,sliceIdx
        if self.lengthPoints.addPoint(coordinates): # if did not already exist
            currentPolygonActor = self.lengthPoints.generatePolygonLastPoint(pickedCoordinates) # generate polygon for the point we just added
            self.renderer.AddActor(currentPolygonActor)

            for point in self.lengthPoints.points:
                polygon = point.polygon
                polygon.GeneratePolygonOn()
                self.renderWindow.Render()

    def _save_file(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Length Points As", CFG.get_config_data("folders", 'default-save-to-folder'),
                "%s Files (*.%s)" % ("json".upper(), "json"))

        if fileName:
            logging.info(f'Saving length/MPR points to {fileName}')
            self.model.saveLengths(fileName, self.lengthPoints)
