# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'window1.6.ui'
# Created by: PyQt5 UI code generator 5.13.0

from PyQt5 import QtCore, QtGui, QtWidgets
import AxialCoronalViewer
import ViewerProp
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import getMPR
from MPRWindow import Ui_MPRWindow
import glob
import os
from getListOfFiles import getListOfFiles
import pickle
import numpy as np
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showFullScreen()
        MainWindow.showMaximized()
        MainWindow.setStyleSheet("background-color: rgb(171, 216, 255);\n"
                                 "border-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 5, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.showMaximized()
        # self.groupBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Coronallabel = QtWidgets.QLabel(self.groupBox)
        self.Coronallabel.setObjectName("Coronallabel")
        self.gridLayout_4.addWidget(self.Coronallabel, 2, 0, 1, 1)
        self.AxialSeqBox = QtWidgets.QComboBox(self.groupBox)
        self.AxialSeqBox.setObjectName("AxialSeqBox")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AxialSeqBox.sizePolicy().hasHeightForWidth())
        self.AxialSeqBox.setSizePolicy(sizePolicy)
        # self.AxialSeqBox.addItem("")
        # self.AxialSeqBox.addItem("")
        # self.AxialSeqBox.addItem("")
        # self.AxialSeqBox.addItem("")
        self.gridLayout_4.addWidget(self.AxialSeqBox, 1, 1, 1, 1)
        self.CoronalSeqBox = QtWidgets.QComboBox(self.groupBox)
        self.CoronalSeqBox.setObjectName("CoronalSeqBox")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CoronalSeqBox.sizePolicy().hasHeightForWidth())
        self.CoronalSeqBox.setSizePolicy(sizePolicy)

        # self.CoronalSeqBox.addItem("")
        # self.CoronalSeqBox.addItem("")
        # self.CoronalSeqBox.addItem("")
        # self.CoronalSeqBox.addItem("")
        self.gridLayout_4.addWidget(self.CoronalSeqBox, 2, 1, 1, 1)
        self.Axiallabel = QtWidgets.QLabel(self.groupBox)
        self.Axiallabel.setObjectName("Axiallabel")
        self.gridLayout_4.addWidget(self.Axiallabel, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 4, 1, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.groupBox)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_4.addWidget(self.line_4, 4, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.groupBox)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_4.addWidget(self.line_3, 4, 0, 1, 1)
        # self.UpLowBox = QtWidgets.QComboBox(self.groupBox)
        # self.UpLowBox.setObjectName("UpLowBox")
        # self.UpLowBox.addItem("")
        # self.UpLowBox.addItem("")
        # self.gridLayout_4.addWidget(self.UpLowBox, 3, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_4.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.window_label = QtWidgets.QLabel(self.groupBox)
        self.window_label.setObjectName("window_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.window_label)
        self.spinBoxWindow = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxWindow.setMinimum(-9999)
        self.spinBoxWindow.setMaximum(9999)
        self.spinBoxWindow.setProperty("value", 1600)
        self.spinBoxWindow.setObjectName("spinBoxWindow")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxWindow)
        self.level_label = QtWidgets.QLabel(self.groupBox)
        self.level_label.setObjectName("level_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.level_label)
        self.spinBoxLevel = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxLevel.setMinimum(-9999)
        self.spinBoxLevel.setMaximum(9999)
        self.spinBoxLevel.setProperty("value", 800)
        self.spinBoxLevel.setObjectName("spinBoxLevel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxLevel)
        self.gridLayout_4.addLayout(self.formLayout, 5, 1, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 6, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 1, 1, 1)
        self.CoronalFrame = QtWidgets.QGroupBox(self.centralwidget)
        self.CoronalFrame.setObjectName("CoronalFrame")
        self.CoronalFrame.showMaximized()
        self.gridLayout_3.addWidget(self.CoronalFrame, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 2, 1, 1)
        self.AxialFrame = QtWidgets.QGroupBox(self.centralwidget)
        self.AxialFrame.showMaximized()
        self.AxialFrame.setObjectName("AxialFrame")
        # self.gridLayout_3.addWidget(self.AxialFrame, 1, 5, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 3, 1, 1)

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.Calculate = QtWidgets.QPushButton(self.groupBox_2)
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
        self.gridLayout_3.addWidget(self.groupBox_2, 3, 5, 1, 1)

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
        self.ViewerProperties = ViewerProp.viewerLogic(self.FilesList,str(self.AxialSeqBox.currentIndex()),
                                                       str(self.CoronalSeqBox.currentIndex()))

        # display axial viewer
        AxialVTKQidget = QVTKRenderWindowInteractor(self.AxialFrame)
        self.gridLayout_3.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        self.AxialViewer = AxialCoronalViewer.PlaneViewerQT(AxialVTKQidget, self.ViewerProperties, 'Axial')

        # dispaly coronal viewer

        CoronalVTKQidget = QVTKRenderWindowInteractor(self.CoronalFrame)
        self.gridLayout_3.addWidget(CoronalVTKQidget, 1, 1, 1, 1)
        self.CoronalViewer = AxialCoronalViewer.PlaneViewerQT(CoronalVTKQidget, self.ViewerProperties, 'Coronal')



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "R"))
        self.label_7.setText(_translate("MainWindow", "P"))
        self.groupBox.setTitle(_translate("MainWindow", "Settings"))
        self.Axiallabel.setText(_translate("MainWindow", "Axial"))
        self.Coronallabel.setText(_translate("MainWindow", "Coronal"))
        self.level_label.setText(_translate("MainWindow", "Level"))
        self.window_label.setText(_translate("MainWindow", "Window"))
        self.pushButton_2.setText(_translate("MainWindow", "Update"))
        self.label_6.setText(_translate("MainWindow", "L"))
        self.label_8.setText(_translate("MainWindow", "I"))
        self.label_2.setText(_translate("MainWindow", "S (Coronal)"))
        self.label.setText(_translate("MainWindow", "A (Axial)"))
        self.label_4.setText(_translate("MainWindow", "L"))
        self.label_9.setText(_translate("MainWindow", "R"))
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
            self.AxialSeqBox.addItem(basename)
            self.CoronalSeqBox.addItem(basename)

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
