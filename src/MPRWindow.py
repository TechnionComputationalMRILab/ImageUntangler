# -*- coding: utf-8 -*-
# refactored code of generated code from ui file 'window1.6.ui'
# generator was by: PyQt5 UI code generator 5.13.0


from PyQt5.QtCore import QRect, QSize, QCoreApplication, QMetaObject
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QSizePolicy, QVBoxLayout, QPushButton, QLabel,QDoubleSpinBox, \
    QMenuBar, QSpinBox, QStatusBar, QFileDialog, QMainWindow, QApplication
import numpy as np
from collections import namedtuple
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import getMPR
import MPRViewer
import MPRViewerProperties
import pickle, sys
from typing import List
from icecream import ic

LengthResults = namedtuple("LengthResults", "totalDistance allDistances")


class Ui_MPRWindow:
    def buildMainWindow(self, MPRWindow):
        MPRWindow.setObjectName("MainWindow")
        MPRWindow.resize(990, 797)
        MPRWindow.setMaximumSize(QSize(990, 16777215))
        self.centralwidget = QWidget(MPRWindow)
        self.centralwidget.setObjectName("centralwidget")
        MPRWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MPRWindow)
        self.menubar.setGeometry(QRect(0, 0, 990, 22))
        self.menubar.setObjectName("menubar")
        MPRWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MPRWindow)
        self.statusbar.setObjectName("statusbar")
        MPRWindow.setStatusBar(self.statusbar)

    def _buildCommonSizePolicy(self, heightDependsOnWidth: bool):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(heightDependsOnWidth)
        return sizePolicy
    
    def buildLengthCalcBox(self):
        self.lengthCalcBox = QGroupBox(self.centralwidget)
        self.lengthCalcBox.setSizePolicy(self._buildCommonSizePolicy(self.lengthCalcBox.sizePolicy().hasHeightForWidth()))
        self.lengthCalcBox.setObjectName("lengthCalcBox")
        self.verticalLayout = QVBoxLayout(self.lengthCalcBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setPointsButton = QPushButton(self.lengthCalcBox)
        self.setPointsButton.setObjectName("setPointsButton")
        self.verticalLayout.addWidget(self.setPointsButton, 0, QtCore.Qt.AlignHCenter)
        self.calcLengthButton = QPushButton(self.lengthCalcBox)
        self.calcLengthButton.setObjectName("calcLengthButton")
        self.verticalLayout.addWidget(self.calcLengthButton, 0, QtCore.Qt.AlignHCenter)
        self.saveButton = QPushButton(self.lengthCalcBox)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton, 0, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.lengthCalcBox, 1, 1, 1, 1)
    
    def buildLengthResultsBox(self):
        self.lengthResultsBox = QGroupBox(self.centralwidget)
        self.lengthResultsBox.setSizePolicy(
            self._buildCommonSizePolicy(self.lengthResultsBox.sizePolicy().hasHeightForWidth()))
        self.lengthResultsBox.setObjectName("lengthResultsBox")
        self.lengthResultsLayout = QVBoxLayout(self.lengthResultsBox)
        self.lengthResultsLayout.setObjectName("lengthResultsLayout")
        self.lengthResultsLabel = QLabel(self.lengthResultsBox)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lengthResultsLabel.setFont(font)
        self.lengthResultsLabel.setObjectName("lengthResultsLabel")
        self.lengthResultsLayout.addWidget(self.lengthResultsLabel, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.mainLayout.addWidget(self.lengthResultsBox, 1, 2, 1, 1)
    
    def buildSizeSettingsBox(self):
        self.sizeSettingBox = QGroupBox(self.centralwidget)
        self.sizeSettingBox.setObjectName("sizeSettingBox")
        self.settingsBoxLayout = QGridLayout(self.sizeSettingBox)
        self.settingsBoxLayout.setObjectName("settingsBoxLayout")
        self.angleLabel = QLabel(self.sizeSettingBox)
        self.angleLabel.setObjectName("angleLabel")
        self.settingsBoxLayout.addWidget(self.angleLabel, 1, 0, 1, 1)
        self.heightSetter = QDoubleSpinBox(self.sizeSettingBox)
        self.heightSetter.setMaximum(5000.0)
        self.heightSetter.setProperty("value", 20.0)
        self.heightSetter.setObjectName("heightSetter")
        self.settingsBoxLayout.addWidget(self.heightSetter, 0, 1, 1, 1)
        self.label = QLabel(self.sizeSettingBox)
        self.label.setObjectName("label")
        self.settingsBoxLayout.addWidget(self.label, 0, 0, 1, 1)
        self.unitsLabel = QLabel(self.sizeSettingBox)
        self.unitsLabel.setObjectName("unitsLabel")
        self.settingsBoxLayout.addWidget(self.unitsLabel, 0, 2, 1, 1)
        self.degreeLabel = QLabel(self.sizeSettingBox)
        self.degreeLabel.setObjectName("degreeLabel")
        self.settingsBoxLayout.addWidget(self.degreeLabel, 1, 2, 1, 1)
        self.updateButton = QPushButton(self.sizeSettingBox)
        self.updateButton.setObjectName("updateButton")
        self.settingsBoxLayout.addWidget(self.updateButton, 2, 1, 1, 1)
        self.angleSetter = QSpinBox(self.sizeSettingBox)
        self.angleSetter.setMaximum(180)
        self.angleSetter.setObjectName("angleSetter")
        self.settingsBoxLayout.addWidget(self.angleSetter, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.sizeSettingBox, 1, 0, 1, 1)
    
    def buildMainViewerBox(self):
        self.mainViewerBox = QGroupBox(self.centralwidget)
        self.mainViewerBox.setSizePolicy(self._buildCommonSizePolicy(self.mainViewerBox.sizePolicy().hasHeightForWidth()))
        self.mainViewerBox.setFlat(False)
        self.mainViewerBox.setCheckable(False)
        self.mainViewerBox.setObjectName("mainViewerBox")
        self.mainLayout.addWidget(self.mainViewerBox, 0, 0, 1, 3)

    def buildMainLayout(self):
        self.mainLayout = QGridLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.mainLayout.setColumnStretch(2, 2)
        self.mainLayout.setRowStretch(0, 4)
        self.mainLayout.setRowStretch(1, 1)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lengthCalcBox.setTitle(_translate("MainWindow", "Calculate Distance"))
        self.setPointsButton.setText(_translate("MainWindow", "Set Points"))
        self.calcLengthButton.setText(_translate("MainWindow", "Calculate Length"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.lengthResultsBox.setTitle(_translate("MainWindow", "Result"))
        self.sizeSettingBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.angleLabel.setText(_translate("MainWindow", "Angle"))
        self.label.setText(_translate("MainWindow", "Height"))
        self.unitsLabel.setText(_translate("MainWindow", "[mm]"))
        self.degreeLabel.setText(_translate("MainWindow", "deg"))
        self.updateButton.setText(_translate("MainWindow", "Update"))
        self.mainViewerBox.setTitle(_translate("MainWindow", "MPR"))


    
    def LoadViewer(self, MPR_M, delta, MPRposition, points, ConvViewerProperties, Height, angle,ConvViewMode):
        self.MPRViewerProperties = MPRViewerProperties.viewerLogic(MPR_M, delta, MPRposition, points, Height, angle, ConvViewerProperties, ConvViewMode)
        self.interactor = QVTKRenderWindowInteractor(self.mainViewerBox)
        self.mainLayout.addWidget(self.interactor, 0, 0, 1, 3)
        self.MPR_Viewer = MPRViewer.View(self.interactor, self.MPRViewerProperties)

    def setupUi(self, MPRWindow, MPR_M, delta, MPRposition, ConvViewerProperties, points, ConvViewMode):
        ic(delta)
        self.buildMainWindow(MPRWindow) # build widgets and qualities of MPR window
        self.buildMainLayout() # set basic dimensions of MPR window
        self.buildLengthCalcBox() # build box in lower center with length calculating options
        self.buildLengthResultsBox() # builds box in lower right that holds the results of the length calculations
        self.buildSizeSettingsBox() # builds box with resizin options
        self.buildMainViewerBox() # builds holder for MPR image
        self.retranslateUi(MPRWindow) # add text to all widgets
        QMetaObject.connectSlotsByName(MPRWindow)
        self.LoadViewer(MPR_M, delta,MPRposition, points, ConvViewerProperties, self.heightSetter.value(), self.angleSetter.value(), ConvViewMode) # builds MPR viewer
        self.connectButtons() # connects all buttons to their relevant functions


    def HeightChanged(self):
        self.MPRViewerProperties.MPRHeight = self.heightSetter.value()
        self.MPRViewerProperties.Angle = self.angleSetter.value()
        self.GetMPR = getMPR.PointsToPlansVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.originalPoints, self.MPRViewerProperties.ConvViewMode, height=self.MPRViewerProperties.MPRHeight,
                                                  viewAngle=self.MPRViewerProperties.Angle, Plot=0)
        self.MPRViewerProperties.MPR_M = self.GetMPR.MPR_M
        self.MPRViewerProperties.delta = self.GetMPR.delta
        self.MPRViewerProperties.MPRposition = self.GetMPR.MPR_indexs_np
        self.MPR_Viewer.Visualize_MPR()
    
    def SaveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.mainViewerBox, "QFileDialog.getSaveFileName()", "", options=options)
        outfile = open(fileName, 'wb')
        pickle.dump([self.MPRViewerProperties.originalPoints, self.MPRViewerProperties.ConvViewerProperties.CoronalArrayDicom,
                     self.MPRViewerProperties.DistancePickingindices, self.MPRViewerProperties.ConvViewerProperties.CorPath], outfile)
        outfile.close()

    def setPointsButtonClick(self):
        if self.MPR_Viewer.interactorStyle.actions["Picking"] == 0:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 1
            self.setPointsButton.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 0
            self.setPointsButton.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

    def generateIndices(self, lengthPoints, delta) -> List[List[int]]:
        return [[int(point.coordinates[0] // self.MPRViewerProperties.delta), int(point.coordinates[1] // delta)]
                for point in lengthPoints.points]
    
    def outputLengthResults(self, lengthResults: LengthResults):
        strdis = ["{0:.2f}".format(lengthResults.allDistances[i]) for i in range(len(lengthResults.allDistances))]
        self.lengthResultsLabel.setText(
            "The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),
                                                                                 "{0:.2f}".format(lengthResults.totalDistance)))
        self.lengthResultsLabel.adjustSize()
        
    def calculateDistances(self) -> None:
        # calculate and output distance of length points in MPR Viewer
        #self.MPRViewerProperties.DistancePickingIndexs = self.MPR_Viewer.lengthPoints.points
        #indices = self.MPRViewerProperties.DistancePickingIndexs
        indices = self.generateIndices(self.MPR_Viewer.lengthPoints, self.MPRViewerProperties.delta)
        MPR_Position = self.MPRViewerProperties.MPRposition
        ic(indices)
        pointsPositions = [ MPR_Position[indices[i][0], indices[i][1],:] for i in range(len(indices))]
        pointsPositions = np.asarray(pointsPositions)
        allLengths = [np.linalg.norm(pointsPositions[j,:] - pointsPositions[j+1,:]) for j in range(len(pointsPositions)-1)]
        totalDistance = np.sum(allLengths)
        self.outputLengthResults(LengthResults(totalDistance=totalDistance, allDistances=allLengths))

        

    def connectButtons(self):
        self.updateButton.clicked.connect(lambda: self.HeightChanged())
        self.saveButton.clicked.connect(lambda: self.SaveFile())
        self.setPointsButton.clicked.connect(lambda: self.setPointsButtonClick())
        self.calcLengthButton.clicked.connect(lambda: self.calculateDistances())



if __name__ == "__main__":
    app = QApplication([])
    MPRWindow = QMainWindow()
    ui = Ui_MPRWindow()
    ui.setupUi(MPRWindow)
    MPRWindow.show()
    sys.exit(app.exec_())
