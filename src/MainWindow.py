# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'window1.6.ui'
# Created by: PyQt5 UI code generator 5.13.0

import os, pickle, numpy as np
from typing import List, Tuple
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QComboBox, QSizePolicy, QFrame, \
    QPushButton, QFormLayout, QSpinBox


from MPRWindow import Ui_MPRWindow
import getMPR
import AxialCoronalViewer
import ViewerProp
from getListOfFiles import getListOfFiles


class Ui_MainWindow:
    def buildMainWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.showFullScreen()
        MainWindow.showMaximized()
        MainWindow.setStyleSheet("background-color: rgb(171, 216, 255);\n"
                                 "border-color: rgb(0, 0, 0);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

    def buildMainLayoutManager(self):
        self.mainLayout = QGridLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def _getCommonFont(self) -> QFont:
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        return font

    def commonLabel(self, obj_name: str, font: QFont, alignment=None) -> QLabel:
        #Shortens process of creating new label with central widget as its parent
        cur_label = QLabel(self.centralwidget)
        cur_label.setObjectName(obj_name)
        if font is not None:
            cur_label.setFont(font)
        if alignment is not None:
            cur_label.setAlignment(QtCore.Qt.AlignCenter)
        return cur_label

    def buildImageBoundaries(self):
        boundaries: List[Tuple[QLabel, str]] = [(self.leftLeftBoundary, "leftLeftBoundary"), (self.leftRightBoundary, "leftRightBoundary"),
                      (self.rightLeftBoundary, "rightLeftBoundary"), (self.rightRightBoundary, "rightLeftBoundary")]
        for boundary in boundaries:
            curBoundary = self.commonLabel(boundary[1], self._getCommonFont()())
            boundary[0] = curBoundary

        self.mainLayout.addWidget(self.leftLeftBoundary, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.leftRightBoundary, 1, 2, 1, 1)
        self.mainLayout.addWidget(self.rightLeftBoundary, 1, 4, 1, 1)
        self.mainLayout.addWidget(self.rightRightBoundary, 1, 6, 1, 1)

    def _buildSizePolicy(self, titleBox: QComboBox):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(titleBox.sizePolicy().hasHeightForWidth())

    def buildImageLists(self):
        self.AxialImagesList = QComboBox(self.groupBox)
        self.AxialImagesList.setObjectName("AxialImagesList")
        self.AxialImagesList.setSizePolicy(self._buildSizePolicy())
        self.settingsLayout.addWidget(self.AxialImagesList, 1, 1, 1, 1)
        self.CoronalImagesList = QComboBox(self.groupBox)
        self.CoronalImagesList.setObjectName("CoronalImagesList")
        self.CoronalImagesList.setSizePolicy(self._buildSizePolicy(self.CoronalImagesList))
        self.settingsLayout.addWidget(self.CoronalImagesList, 2, 1, 1, 1)

    def _setGroupBox(self):
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.showMaximized()
        # self.groupBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox.setObjectName("groupBox")

    def buildSettingsLayoutManager(self):
        self.settingsLayout = QGridLayout(self.groupBox)
        self.settingsLayout.setObjectName("settingsLayout")

    def _setCoronalLabel(self):
        self.Coronallabel = self.commonLabel("Coronallabel")
        self.settingsLayout.addWidget(self.Coronallabel, 2, 0, 1, 1)


    def _setAxialLabel(self):
        self.Axiallabel = self.commonLabel("Axiallabel")
        self.settingsLayout.addWidget(self.Axiallabel, 1, 0, 1, 1)

    def buildFrame(self, obj_name):
        curFrame = QFrame(self.groupBox)
        curFrame.setFrameShape(QtWidgets.QFrame.HLine)
        curFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        curFrame.setObjectName(obj_name)
        return curFrame

    def _setLi2(self):
        self.line_2 = self.buildFrame("line_2")
        self.settingsLayout.addWidget(self.line_2, 4, 1, 1, 1)

    def _setLi4(self):
        self.line_4 = self.buildFrame("line_4")
        self.settingsLayout.addWidget(self.line_4, 4, 2, 1, 1)

    def _setLi3(self):
        self.line_3 = self.buildFrame("line_3")
        self.settingsLayout.addWidget(self.line_3, 4, 0, 1, 1)

    def _setPb2(self):
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.settingsLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)

    def _setFl(self):
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.window_label = QLabel(self.groupBox)
        self.window_label.setObjectName("window_label")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.window_label)

    def _setSB1(self):
        self.spinBoxWindow = QSpinBox(self.groupBox)
        self.spinBoxWindow.setMinimum(-9999)
        self.spinBoxWindow.setMaximum(9999)
        self.spinBoxWindow.setProperty("value", 1600)
        self.spinBoxWindow.setObjectName("spinBoxWindow")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBoxWindow)

    def _setll1(self):
        self.level_label = QLabel(self.groupBox)
        self.level_label.setObjectName("level_label")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.level_label)

    def _setSB2(self):
        self.spinBoxLevel = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxLevel.setMinimum(-9999)
        self.spinBoxLevel.setMaximum(9999)
        self.spinBoxLevel.setProperty("value", 800)
        self.spinBoxLevel.setObjectName("spinBoxLevel")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBoxLevel)

    def underBoundaries(self):
        self.pLabel = self.getCommonLabel("pLabel", self._getCommonFont()(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.pLabel, 2, 5, 1, 1)
        self.iLabel = self.getCommonLabel("iLabel", self._getCommonFont()(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.label_8, 2, 1, 1, 1)

    def _setCoronalFrame(self):
        self.CoronalFrame = QGroupBox(self.centralwidget)
        self.CoronalFrame.setObjectName("CoronalFrame")
        self.CoronalFrame.showMaximized()
        self.mainLayout.addWidget(self.CoronalFrame, 1, 1, 1, 1)

    def _setL2(self):
        self.label_2 = QLabel(self.centralwidget)
        font = self._getCommonFont()()
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.mainLayout.addWidget(self.label_2, 0, 1, 1, 1)

    def _setL(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = self._getCommonFont()()
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.mainLayout.addWidget(self.label, 0, 5, 1, 1)

    def _setLi(self):
        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainLayout.addWidget(self.line, 1, 3, 1, 1)

    def _setGb2(self):
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")

    def setupUi(self, MainWindow):
        self.buildMainWindow(MainWindow)
        self.buildMainLayoutManager()
        self.buildImageBoundaries() # Sets L/R marking on sides of NRRM images

        self._setGroupBox()
        self.buildSettingsLayoutManager()
        self._setCoronalLabel()
        self.buildImageLists()
        self._setAxialLabel()
        self._setLi2()
        self._setLi4()
        self._setLi3()
        self._setPb2()
        self._setFl()
        self._setSB1()
        self._setll1()
        self.settingsLayout.addLayout(self.formLayout, 5, 1, 1, 1)
        self.mainLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        self._setCoronalFrame()
        self._setL2()
        self._setL()
        #?
        self.AxialFrame = QGroupBox(self.centralwidget)
        self.AxialFrame.showMaximized()
        self.AxialFrame.setObjectName("AxialFrame")
        # self.mainLayout.addWidget(self.AxialFrame, 1, 5, 1, 1)
        self._setLi()

        self._setGb2()
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.Calculate = QPushButton(self.groupBox_2)
        self.Calculate.setObjectName("Newpoint")
        self.gridLayout.addWidget(self.Calculate, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 6, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 2, 1, 1)



        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        # self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.mainLayout.addWidget(self.groupBox_2, 3, 5, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("""QMenuBar { background-color: rgb(236, 232, 232); }""")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setStyleSheet("""QMenu { background-color: rgb(236, 232, 232); }""")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.OpenFolder)
        self.menuFile.addAction(self.actionNew)
        self.menubar.addAction(self.menuFile.menuAction())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # preperviewer
        self.OpenFolder()
        self.LoadViewer()

        self.spinBoxWindow.setValue(self.ViewerProperties.WindowVal)
        self.spinBoxLevel.setValue(self.ViewerProperties.LevelVal)
        # self.UpLowBox.currentIndexChanged[str].connect(self.LoadViewer())
        self.pushButton_2.clicked.connect(lambda: self.LoadViewer())
        self.spinBoxWindow.valueChanged.connect(lambda: self.WindowLevelUpdate())
        self.spinBoxLevel.valueChanged.connect(lambda: self.WindowLevelUpdate())
        self.pushButton.clicked.connect(lambda: self.PickPointsStatus())
        self.pushButton_5.clicked.connect(lambda: self.PickPointsCalcStatus())
        self.Calculate.clicked.connect(lambda: self.calc_clicked())
        self.pushButton_4.clicked.connect(lambda: self.CalculateDis())

    def WindowLevelUpdate(self):
        self.AxialViewer.visualizationWindow =  self.spinBoxWindow.value()
        self.AxialViewer.visualizationLevel = self.spinBoxLevel.value()
        self.AxialViewer.UpdateWindowLevel_Val()


        self.CoronalViewer.visualizationWindow =  self.spinBoxWindow.value()
        self.CoronalViewer.visualizationLevel = self.spinBoxLevel.value()
        self.CoronalViewer.UpdateWindowLevel_Val()

    def LoadViewer(self):
        self.ViewerProperties = ViewerProp.viewerLogic(self.FilesList,str(self.AxialImagesList.currentIndex()),
                                                       str(self.CoronalImagesList.currentIndex()))

        # display axial viewer
        AxialVTKQidget = QVTKRenderWindowInteractor(self.AxialFrame)
        self.mainLayout.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        self.AxialViewer = AxialCoronalViewer.PlaneViewerQT(AxialVTKQidget, self.ViewerProperties, 'Axial')

        # dispaly coronal viewer

        CoronalVTKQidget = QVTKRenderWindowInteractor(self.CoronalFrame)
        self.mainLayout.addWidget(CoronalVTKQidget, 1, 1, 1, 1)
        self.CoronalViewer = AxialCoronalViewer.PlaneViewerQT(CoronalVTKQidget, self.ViewerProperties, 'Coronal')



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rightLeftBoundary.setText(_translate("MainWindow", "R"))
        self.pLabel.setText(_translate("MainWindow", "P"))
        self.groupBox.setTitle(_translate("MainWindow", "Settings"))
        self.Axiallabel.setText(_translate("MainWindow", "Axial"))
        self.Coronallabel.setText(_translate("MainWindow", "Coronal"))
        self.level_label.setText(_translate("MainWindow", "Level"))
        self.window_label.setText(_translate("MainWindow", "Window"))
        self.pushButton_2.setText(_translate("MainWindow", "Update"))
        self.rightRightBoundary.setText(_translate("MainWindow", "L"))
        self.label_8.setText(_translate("MainWindow", "I"))
        self.label_2.setText(_translate("MainWindow", "S (Coronal)"))
        self.label.setText(_translate("MainWindow", "A (Axial)"))
        self.leftLeftBoundary.setText(_translate("MainWindow", "L"))
        self.leftRightBoundary.setText(_translate("MainWindow", "R"))
        self.Calculate.setText(_translate("MainWindow", "Calculate MPR"))
        self.pushButton.setText(_translate("MainWindow", "Set Points - Calculate MPR"))
        # self.pushButton_3.setText(_translate("MainWindow", "Display Cursor"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.pushButton_4.setText(_translate("MainWindow", "Calculate Length"))
        self.pushButton_5.setText(_translate("MainWindow", "Set Points - Calculate Length"))

    def OpenFolder(self):
        FolderPath = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.FilesList = getListOfFiles(FolderPath)
        for i in range(len(self.FilesList)):
            basename = os.path.basename(self.FilesList[i])
            basename = basename[:-5]
            self.AxialImagesList.addItem(basename)
            self.CoronalImagesList.addItem(basename)

    def calc_clicked(self):
        # print("in Window: ", self.CoronalViewer.PickingPointsIm)
        ListOfPoints = self.CoronalViewer.PickingPointsIm
        ViewMode = 'Coronal'
        plot =0
        #Hight [mm]
        # outfile = open(r'D:\FinalProject\Data_moti\Case007\viewer_prop', 'wb')
        # pickle.dump([self.ViewerProperties.CoronalArrayDicom, self.ViewerProperties.CoronalVTKOrigin,
                     # self.ViewerProperties.CoronalVTKSpacing, self.ViewerProperties.CoronalDimensions], outfile)
        # outfile.close()
        GetMPR = getMPR.PointsToPlansVectors(self.ViewerProperties, ListOfPoints, ViewMode, Plot = plot,Height = 40, viewAngle = 180)
        MPR_M = GetMPR.MPR_M
        delta = GetMPR.delta
        MPRPosiotion = GetMPR.MPR_indexs_np
        self.openMPRWindow(MPR_M,delta,MPRPosiotion,ListOfPoints,ViewMode)

        # fileName = self.ViewerProperties.CorPath + "\sampledata"
        # outfile = open(fileName, 'wb')
        # # np.savetxt(name1, self.MPRViewerProperties.ListOfPoints_Original,header=self.MPRViewerProperties.ConvViewerProperties.CorPath)
        # pickle.dump([GetMPR.ListOfPoints_Original,
        #              GetMPR.ConvViewerProperties.CoronalArrayDicom,
        #              GetMPR.x,GetMPR.y, GetMPR.z,], outfile)
        # outfile.close()

    def openMPRWindow(self,MPR_M,delta,MPRPosiotion,ListOfPoints,ViewMode):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MPRWindow()
        # ListOfPoints = self.CoronalViewer.PickingPointsIm
        # ViewMode = 'Coronal'
        self.ui.setupUi(self.window, MPR_M, delta,MPRPosiotion,self.ViewerProperties,ListOfPoints,ViewMode)
        self.window.show()

    def PickPointsStatus(self):
        # print("PushButten clicked")
        if self.CoronalViewer.interactorStyle.actions["PickingMPR"] == 0:
            self.CoronalViewer.interactorStyle.actions["PickingMPR"] = 1
            self.pushButton.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.CoronalViewer.interactorStyle.actions["PickingMPR"] = 0
            self.pushButton.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

    def PickPointsCalcStatus(self):
        # print("PushButten clicked")
        if self.CoronalViewer.interactorStyle.actions["PickingLength"] == 0:
            self.CoronalViewer.interactorStyle.actions["PickingLength"] = 1
            self.pushButton_5.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.CoronalViewer.interactorStyle.actions["PickingLength"] = 0
            self.pushButton_5.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

    def CalculateDis(self):
        DistancePickingIndexs = self.CoronalViewer.LenPickingPointsIm
        DistancePickingIndexs = np.asarray(DistancePickingIndexs)
        Alldis = []

        for j in range(len(DistancePickingIndexs)-1):
            diff = DistancePickingIndexs[j+1,0:3] - DistancePickingIndexs[j,0:3]
            dis = np.linalg.norm(diff)
            Alldis.append(dis)
        Alldis = np.asarray(Alldis)

        TotlalD = np.sum(Alldis)
        strdis = ["{0:.2f}".format(Alldis[i]) for i in range(len(Alldis))]
        self.label_5.setText("The lengths [mm] are: {0} \n\nThe total length: {1}".format(' , '.join(strdis),"{0:.2f}".format(TotlalD)))
        # self.GetMPR.PlotSelectedPointsForDis(Points_Position)
        self.label_5.adjustSize()


        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.groupBox, "QFileDialog.getSaveFileName()", "",
                                                            options=options)
        print(fileName)
        if fileName!="":
            outfile = open(fileName, 'wb')
            pickle.dump([DistancePickingIndexs, Alldis], outfile)
            outfile.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
