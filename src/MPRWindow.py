# -*- coding: utf-8 -*-
# refactored code of generated code from ui file 'window1.6.ui'
# generator was by: PyQt5 UI code generator 5.13.0


from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QSizePolicy, QVBoxLayout, QPushButton, QLabel,QDoubleSpinBox, \
    QMenuBar, QSpinBox, QStatusBar, QFileDialog, QMainWindow, QApplication
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import getMPR
import MPRViewer
import MPRViwerProp
import pickle, sys


class Ui_MPRWindow:

    def buildMainWindow(self, MPRWindow):
        MPRWindow.setObjectName("MainWindow")
        MPRWindow.resize(990, 797)
        MPRWindow.setMaximumSize(QtCore.QSize(990, 16777215))
        self.centralwidget = QWidget(MPRWindow)
        self.centralwidget.setObjectName("centralwidget")

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
        self.mainViewerBox.setObjectName("groupBox")
        self.mainLayout.addWidget(self.mainViewerBox, 0, 0, 1, 3)

    def buildMainLayout(self):
        self.mainLayout = QGridLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.mainLayout.setColumnStretch(2, 2)
        self.mainLayout.setRowStretch(0, 4)
        self.mainLayout.setRowStretch(1, 1)

        
    def setupUi(self, MPRWindow, MPR_M, delta, MPRPosiotion, ConvViewerProperties, ListOfPoints, ConvViewMode):
        self.buildMainWindow(MPRWindow)

        self.buildMainLayout()
        self.buildLengthCalcBox()
        self.buildLengthResultsBox()
        self.buildSizeSettingsBox()
        self.buildMainViewerBox()



        MPRWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MPRWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 990, 22))
        self.menubar.setObjectName("menubar")
        MPRWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MPRWindow)
        self.statusbar.setObjectName("statusbar")
        MPRWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MPRWindow)
        QtCore.QMetaObject.connectSlotsByName(MPRWindow)


        # self.Visualize_MPR(MPR_M,delta)


        Height = self.heightSetter.value()
        angle = self.angleSetter.value()

        self.LoadViewer(MPR_M, delta,MPRPosiotion, ListOfPoints, ConvViewerProperties,Height, angle,ConvViewMode)


        self.updateButton.clicked.connect(lambda: self.HeightChanged())
        self.saveButton.clicked.connect(lambda: self.SaveFile())
        self.setPointsButton.clicked.connect(lambda: self.setPointsButtonClick())
        self.calcLengthButton.clicked.connect(lambda: self.CalculateDis())



    def LoadViewer(self, MPR_M, delta,MPRPosiotion, ListOfPoints, ConvViewerProperties, Height, angle,ConvViewMode):

        # self.ViewerProperties = ViewerProp.viewerLogic(self.FolderPath,str(self.UpLowBox.currentText()),str(self.AxialSeqBox.currentText()),
        #                                                str(self.CoronalSeqBox.currentText()), self.angleSetterWindow.value(), self.angleSetterLevel.value())

        # AxialVTKQidget = QVTKRenderWindowInteractor(self.mainViewerBox)
        # self.mainLayout_3.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        # self.AxialViewer = AxialCoronalViewer.PlaneViewerQT(AxialVTKQidget, self.ViewerProperties, 'Axial')
        self.MPRViewerProperties = MPRViwerProp.viewerLogic(MPR_M, delta,MPRPosiotion, ListOfPoints, Height, angle, ConvViewerProperties, ConvViewMode)
        self.interactor = QVTKRenderWindowInteractor(self.mainViewerBox)
        self.mainLayout.addWidget(self.interactor, 0, 0, 1, 3)
        self.MPR_Viewer = MPRViewer.View(self.interactor,self.MPRViewerProperties)


    def HeightChanged(self):
        self.MPRViewerProperties.MPRHeight = self.heightSetter.value()
        self.MPRViewerProperties.Angle = self.angleSetter.value()
        plot = 0
        self.GetMPR = getMPR.PointsToPlansVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.ListOfPoints_Original, self.MPRViewerProperties.ConvViewMode, Height=self.MPRViewerProperties.MPRHeight,
                                             viewAngle=self.MPRViewerProperties.Angle, Plot=plot)
        self.MPRViewerProperties.MPR_M = self.GetMPR.MPR_M
        self.MPRViewerProperties.delta = self.GetMPR.delta
        self.MPRViewerProperties.MPRPosiotion = self.GetMPR.MPR_indexs_np
        self.MPR_Viewer.Visualize_MPR()

    # def AngleChangeByIneractor(self,angle):
    #     self.Hegith = self.heightSetter.value()
    #     self.Angle = angle
    #     plot = 0
    #     GetMPR = getMPR.PointsToPlansVectors(self.ViewerProperties, self.ListOfPoints, self.ViewMode, Heigth=self.Hegith,
    #                                          viewAngle=self.Angle, Plot=plot)
    #     MPR_M = GetMPR.MPR_M
    #     delta = GetMPR.delta
    #     self.angleSetter.setValue(angle)
    #     self.MPR_Viewer.Visualize_MPR(MPR_M, delta)


    def setPointsButtonClick(self):
        if self.MPR_Viewer.interactorStyle.actions["Picking"] == 0:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 1
            self.setPointsButton.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 0
            self.setPointsButton.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")
    def CalculateDis(self):
        self.MPRViewerProperties.DistancePickingIndexs = self.MPR_Viewer.PickingPointsIndex
        Indexs = self.MPRViewerProperties.DistancePickingIndexs
        MPR_Position =self.MPRViewerProperties.MPRPosiotion
        Points_Position = []
        for i in range(len(Indexs)):
            Point = MPR_Position[Indexs[i][0],Indexs[i][1],:]
            Points_Position.append(Point)
        Points_Position = np.asarray(Points_Position)
        self.MPRViewerProperties.PointsForDisCalPosition = Points_Position

        Alldis = []
        for j in range(len(Points_Position)-1):
           dis = np.linalg.norm(Points_Position[j,:] - Points_Position[j+1,:])
           Alldis.append(dis)
        Alldis = np.asarray(Alldis)
        self.MPRViewerProperties.DisCalculate = Alldis

        TotlalD = np.sum(Alldis)
        strdis = ["{0:.2f}".format(Alldis[i]) for i in range(len(Alldis))]
        self.lengthResultsLabel.setText("The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),"{0:.2f}".format(TotlalD)))
        # self.GetMPR.PlotSelectedPointsForDis(Points_Position)
        self.lengthResultsLabel.adjustSize()

    def SaveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.mainViewerBox, "QFileDialog.getSaveFileName()", "", options=options)
        # if fileName:
        #     print(fileName+'.txt')
        # print(self.MPRViewerProperties.ListOfPoints_Original)
        # name1 = fileName+'.txt'
        outfile = open(fileName, 'wb')
        # np.savetxt(name1, self.MPRViewerProperties.ListOfPoints_Original,header=self.MPRViewerProperties.ConvViewerProperties.CorPath)
        pickle.dump([self.MPRViewerProperties.ListOfPoints_Original, self.MPRViewerProperties.ConvViewerProperties.CoronalArrayDicom,
                     self.MPRViewerProperties.DistancePickingIndexs, self.MPRViewerProperties.ConvViewerProperties.CorPath], outfile)
        outfile.close()
        # np.save(name, self.ListOfPoints)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
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



if __name__ == "__main__":
    app = QApplication([])
    MPRWindow = QMainWindow()
    ui = Ui_MPRWindow()
    ui.setupUi(MPRWindow)
    MPRWindow.show()
    sys.exit(app.exec_())
