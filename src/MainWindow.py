# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'window1.6.ui'
# Created by: PyQt5 UI code generator 5.13.0

import os, pickle, numpy as np
from typing import List, Tuple
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QComboBox, QSizePolicy, QFrame, \
    QPushButton, QFormLayout, QSpinBox, QSpacerItem, QMenuBar, QMenu, QAction, QStatusBar


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

    def _buildCommonLabel(self, cur_label: QLabel, obj_name: str, font: QFont, alignment=None) -> QLabel:
        #Shortens process of creating new label with central widget as its parent
        cur_label.setObjectName(obj_name)
        if font is not None:
            cur_label.setFont(font)
        if alignment is not None:
            cur_label.setAlignment(QtCore.Qt.AlignCenter)
        return cur_label

    def buildImageBoundaries(self):
        self.leftLeftBoundary, self.leftRightBoundary, self.rightLeftBoundary, self.rightRightBoundary = QLabel(), QLabel(), QLabel(), QLabel()
        boundaries: List[Tuple[QLabel, str]] = [(self.leftLeftBoundary, "leftLeftBoundary"), (self.leftRightBoundary, "leftRightBoundary"),
                      (self.rightLeftBoundary, "rightLeftBoundary"), (self.rightRightBoundary, "rightLeftBoundary")]
        for boundary in boundaries:
            curBoundary = self._buildCommonLabel(boundary[1], self._getCommonFont())
            boundary[0] = curBoundary

        self.mainLayout.addWidget(self.leftLeftBoundary, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.leftRightBoundary, 1, 2, 1, 1)
        self.mainLayout.addWidget(self.rightLeftBoundary, 1, 4, 1, 1)
        self.mainLayout.addWidget(self.rightRightBoundary, 1, 6, 1, 1)

    def buildSizeSettings(self):
        self.sizeSettingBox = QFormLayout()
        self.sizeSettingBox.setObjectName("sizeSettingBox")
        self.windowSizeCaption = QLabel(self.settingsBox)
        self.windowSizeCaption.setObjectName("windowSizeCaption")
        self.sizeSettingBox.setWidget(0, QFormLayout.LabelRole, self.windowSizeCaption)
        self.levelSizeCaption = QLabel(self.settingsBox)
        self.levelSizeCaption.setObjectName("levelSizeCaption")
        self.sizeSettingBox.setWidget(1, QFormLayout.LabelRole, self.levelSizeCaption)
        self.windowSizeButton = QSpinBox(self.settingsBox)
        self.windowSizeButton.setMinimum(-9999)
        self.windowSizeButton.setMaximum(9999)
        self.windowSizeButton.setProperty("value", 1600)
        self.windowSizeButton.setObjectName("windowSizeButton")
        self.sizeSettingBox.setWidget(0, QFormLayout.FieldRole, self.windowSizeButton)
        self.windowSizeButton.setValue(self.ViewerProperties.WindowVal)
        self.levelSizeButton = QSpinBox(self.settingsBox)
        self.levelSizeButton.setMinimum(-9999)
        self.levelSizeButton.setMaximum(9999)
        self.levelSizeButton.setProperty("value", 800)
        self.levelSizeButton.setObjectName("levelSizeButton")
        self.sizeSettingBox.setWidget(1, QFormLayout.FieldRole, self.levelSizeButton)
        self.levelSizeButton.setValue(self.ViewerProperties.LevelVal)


    def _buildSettingBoxes(self):
        self.Axiallabel = self._commonLabel("Axiallabel")
        self.settingsLayout.addWidget(self.Axiallabel, 1, 0, 1, 1)
        self.Coronallabel = self._commonLabel("Coronallabel")
        self.settingsLayout.addWidget(self.Coronallabel, 2, 0, 1, 1)

    def _buildFrame(self, obj_name):
        curFrame = QFrame(self.settingsBox)
        curFrame.setFrameShape(QtWidgets.QFrame.HLine)
        curFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        curFrame.setObjectName(obj_name)
        return curFrame

    def _buildSettingsFrame(self):
        self.frameBorder1 = self._buildFrame("frameBorder1")
        self.settingsLayout.addWidget(self.frameBorder1, 4, 1, 1, 1)
        self.frameBorder2 = self._buildFrame("frameBorder2")
        self.settingsLayout.addWidget(self.frameBorder2, 4, 2, 1, 1)
        self.frameBorder3 = self._buildFrame("frameBorder3")
        self.settingsLayout.addWidget(self.frameBorder3, 4, 0, 1, 1)

    def _buildUpdateButton(self):
        self.updateButton = QPushButton(self.settingsBox)
        self.updateButton.setObjectName("updateButton")
        self.settingsLayout.addWidget(self.updateButton, 3, 1, 1, 1)


    def _buildSizePolicy(self, titleBox: QComboBox):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(titleBox.sizePolicy().hasHeightForWidth())


    def _buildImageLists(self):
        self.AxialImagesList = QComboBox(self.settingsBox)
        self.AxialImagesList.setObjectName("AxialImagesList")
        self.AxialImagesList.setSizePolicy(self._buildSizePolicy())
        self.settingsLayout.addWidget(self.AxialImagesList, 1, 1, 1, 1)
        self.CoronalImagesList = QComboBox(self.settingsBox)
        self.CoronalImagesList.setObjectName("CoronalImagesList")
        self.CoronalImagesList.setSizePolicy(self._buildSizePolicy(self.CoronalImagesList))
        self.settingsLayout.addWidget(self.CoronalImagesList, 2, 1, 1, 1)

    def buildSettingsLayoutManager(self):
        self.settingsLayout = QGridLayout(self.settingsBox)
        self.settingsLayout.setObjectName("settingsLayout")
        self._buildSettingBoxes()
        self._buildSettingsFrame()
        self._buildUpdateButton()
        self._buildImageLists()

    def buildSettingsBox(self):
        self.settingsBox = QGroupBox(self.centralwidget)
        self.settingsBox.showMaximized()
        self.settingsBox.setObjectName("settingsBox")
        self.buildSizeSettings() # builds the Window and Level size components
        self.buildSettingsLayoutManager() # builds layout manager for most of the box
        self.settingsLayout.addLayout(self.sizeSettingBox, 5, 1, 1, 1) # adds box containing Window/level size spin buttons
        self.mainLayout.addWidget(self.settingsBox, 3, 1, 1, 1) # adds layout containing Setting components to MainWindow



    def underBoundaries(self):
        self.pLabel = self.getCommonLabel("pLabel", self._getCommonFont()(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.pLabel, 2, 5, 1, 1)
        self.iLabel = self.getCommonLabel("iLabel", self._getCommonFont()(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.iLabel, 2, 1, 1, 1)

    def buildCoronalTitle(self):
        self.coronalImageTitle = QLabel(self.centralwidget)
        font = self._getCommonFont()
        self.coronalImageTitle.setFont(font)
        self.coronalImageTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.coronalImageTitle.setObjectName("coronalImageTitle")
        self.mainLayout.addWidget(self.coronalImageTitle, 0, 1, 1, 1)

    def buildCoronalImageFrame(self):
        self.CoronalImageFrame = QGroupBox(self.centralwidget)
        self.CoronalImageFrame.setObjectName("CoronalImageFrame")
        self.CoronalImageFrame.showMaximized()
        self.mainLayout.addWidget(self.CoronalImageFrame, 1, 1, 1, 1)
        self.buildCoronalTitle() # add S (Coronal) title


    def buildAxialTitle(self):
        self.axialTitle = QtWidgets.QLabel(self.centralwidget)
        font = self._getCommonFont()
        self.axialTitle.setAutoFillBackground(False)
        self.axialTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.axialTitle.setObjectName("axialTitle")
        self.mainLayout.addWidget(self.axialTitle, 0, 5, 1, 1)
        self.buildAxialTitle()

    def buildAxialImageFrame(self):
        self.axialImageFrame = QGroupBox(self.centralwidget)
        self.axialImageFrame.showMaximized()
        self.axialImageFrame.setObjectName("axialImageFrame")
        self.buildAxialTitle()
        # self.mainLayout.addWidget(self.axialImageFrame, 1, 5, 1, 1) #? why is this cut out


    def buildImageDivider(self):
        self.imageDivider = QFrame(self.centralwidget)
        self.imageDivider.setFrameShape(QFrame.VLine)
        self.imageDivider.setFrameShadow(QFrame.Sunken)
        self.imageDivider.setObjectName("imageDivider")
        self.mainLayout.addWidget(self.imageDivider, 1, 3, 1, 1)

    def addSpacers(self):
        spacerLeft = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actionsLayout.addItem(spacerLeft, 1, 1, 1, 1)
        spacerRight = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actionsLayout.addItem(spacerRight, 1, 3, 1, 1)

    def buildActionsBox(self):
        self.actionsLayout = QGridLayout(self.dotCalculatingBox)
        self.actionsLayout.setObjectName("actionsLayout")
        self.calcMPRButton = QPushButton(self.dotCalculatingBox)
        self.calcMPRButton.setObjectName("Newpoint")
        self.actionsLayout.addWidget(self.calcMPRButton, 2, 2, 1, 1)
        self.putMPRDotsButton = QtWidgets.QPushButton(self.dotCalculatingBox)
        self.putMPRDotsButton.setObjectName("putMPRDotsButton")
        self.actionsLayout.addWidget(self.putMPRDotsButton, 0, 2, 1, 1)
        self.putLengthDotsButton = QtWidgets.QPushButton(self.dotCalculatingBox)
        self.putLengthDotsButton.setObjectName("putLengthDotsButton")
        self.actionsLayout.addWidget(self.putLengthDotsButton, 4, 2, 1, 1)
        self.calcLengthButton = QtWidgets.QPushButton(self.dotCalculatingBox)
        self.calcLengthButton.setObjectName("calcLengthButton")
        self.actionsLayout.addWidget(self.calcLengthButton, 6, 2, 1, 1)
        self.lengthAnswerTag = QtWidgets.QLabel(self.dotCalculatingBox)
        self.lengthAnswerTag.setObjectName("label_5")
        self.actionsLayout.addWidget(self.lengthAnswerTag, 8, 2, 1, 1)
        self.addSpacers()

    def buildDotCalculatingBox(self):
        self.dotCalculatingBox = QGroupBox(self.centralwidget)
        self.dotCalculatingBox.setTitle("")
        self.dotCalculatingBox.setObjectName("dotCalculatingBox")
        self.buildActionsBox()
        self.mainLayout.addWidget(self.dotCalculatingBox, 3, 5, 1, 1)
    
    def buildStatusBar(self):
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def addFileOpenAction(self):
        self.menuFileAction = QAction(MainWindow)
        self.menuFileAction.setObjectName("menuFileAction")
        self.menuFileAction.triggered.connect(self.OpenFolder)
        self.menuFile.addAction(self.menuFileAction)
        self.menubar.addAction(self.menuFile.menuAction())

    
    def buildMenuBar(self):
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("""QMenuBar { background-color: rgb(236, 232, 232); }""")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setStyleSheet("""QMenu { background-color: rgb(236, 232, 232); }""")
        MainWindow.setMenuBar(self.menubar)
        self.addFileOpenAction()

    def connectAllButtons(self):
        # self.UpLowBox.currentIndexChanged[str].connect(self.LoadViewer())
        self.updateButton.clicked.connect(lambda: self.LoadViewer())
        self.windowSizeButton.valueChanged.connect(lambda: self.WindowLevelUpdate())
        self.levelSizeButton.valueChanged.connect(lambda: self.WindowLevelUpdate())
        self.putMPRDotsButton.clicked.connect(lambda: self.PickPointsStatus())
        self.putLengthDotsButton.clicked.connect(lambda: self.PickPointsCalcStatus())
        self.calcMPRButton.clicked.connect(lambda: self.calc_clicked())
        self.calcLengthButton.clicked.connect(lambda: self.CalculateDis())

    def setupUi(self, MainWindow):
        self.buildMainWindow(MainWindow) # set main window
        self.buildMainLayoutManager()
        self.buildImageBoundaries() # Sets L/R marking on sides of NRRM images
        self.buildSettingsBox() # builds components for 'settings' in the bottom left
        self.buildCoronalImageFrame() # builds frame containing coronal image
        self.buildAxialImageFrame() # builds frame containing axial image
        self.buildImageDivider() # creates line seperating axial and coronal images
        self.buildDotCalculatingBox() # builds box containing buttons for dot-putting calculations
        self.buildStatusBar() # add a status bar at the bottom
        self.buildMenuBar() # add menu at top of screen
        self.retranslateUi(MainWindow) # adds text to all widgets

        QMetaObject.connectSlotsByName(MainWindow) # connect all components to MainWindow

        # open file explorer
        self.OpenFolder()
        self.LoadViewer()

        # connects all buttons to the functions called when they are clicked, updated
        self.connectAllButtons()

    def WindowLevelUpdate(self):
        self.AxialViewer.visualizationWindow =  self.windowSizeButton.value()
        self.AxialViewer.visualizationLevel = self.levelSizeButton.value()
        self.AxialViewer.UpdateWindowLevel_Val()
        self.CoronalViewer.visualizationWindow =  self.windowSizeButton.value()
        self.CoronalViewer.visualizationLevel = self.levelSizeButton.value()
        self.CoronalViewer.UpdateWindowLevel_Val()

    def LoadViewer(self):
        self.ViewerProperties = ViewerProp.viewerLogic(self.FilesList,str(self.AxialImagesList.currentIndex()),
                                                       str(self.CoronalImagesList.currentIndex()))

        # display axial viewer
        AxialVTKQidget = QVTKRenderWindowInteractor(self.axialImageFrame)
        self.mainLayout.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        self.AxialViewer = AxialCoronalViewer.PlaneViewerQT(AxialVTKQidget, self.ViewerProperties, 'Axial')

        # dispaly coronal viewer

        CoronalVTKQidget = QVTKRenderWindowInteractor(self.CoronalImageFrame)
        self.mainLayout.addWidget(CoronalVTKQidget, 1, 1, 1, 1)
        self.CoronalViewer = AxialCoronalViewer.PlaneViewerQT(CoronalVTKQidget, self.ViewerProperties, 'Coronal')



    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # set text to widgets in the center near the images
        self.coronalImageTitle.setText(_translate("MainWindow", "S (Coronal)"))
        self.axialTitle.setText(_translate("MainWindow", "A (Axial)"))
        self.rightLeftBoundary.setText(_translate("MainWindow", "R"))
        self.rightRightBoundary.setText(_translate("MainWindow", "L"))
        self.leftLeftBoundary.setText(_translate("MainWindow", "L"))
        self.leftRightBoundary.setText(_translate("MainWindow", "R"))
        self.pLabel.setText(_translate("MainWindow", "P"))
        self.iLabel.setText(_translate("MainWindow", "I"))
        # set text to widgets in the settings box
        self.settingsBox.setTitle(_translate("MainWindow", "Settings"))
        self.Axiallabel.setText(_translate("MainWindow", "Axial"))
        self.Coronallabel.setText(_translate("MainWindow", "Coronal"))
        self.levelSizeCaption.setText(_translate("MainWindow", "Level"))
        self.windowSizeCaption.setText(_translate("MainWindow", "Window"))
        self.updateButton.setText(_translate("MainWindow", "Update"))
        # set text to widgets in actions box
        self.calcMPRButton.setText(_translate("MainWindow", "Calculate MPR"))
        self.putMPRDotsButton.setText(_translate("MainWindow", "Set Points - Calculate MPR"))
        self.calcLengthButton.setText(_translate("MainWindow", "Calculate Length"))
        self.putLengthDotsButton.setText(_translate("MainWindow", "Set Points - Calculate Length"))
        # set text to widgets in Menu bar
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFileAction.setText(_translate("MainWindow", "New"))


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
            self.putLengthDotsButton.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.CoronalViewer.interactorStyle.actions["PickingLength"] = 0
            self.putLengthDotsButton.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

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
        self.lengthAnswerTag.setText("The lengths [mm] are: {0} \n\nThe total length: {1}".format(' , '.join(strdis),"{0:.2f}".format(TotlalD)))
        # self.GetMPR.PlotSelectedPointsForDis(Points_Position)
        self.lengthAnswerTag.adjustSize()


        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.settingsBox, "QFileDialog.getSaveFileName()", "",
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
