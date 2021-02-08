import os, pickle, sys, sip, numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMetaObject, QCoreApplication, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QComboBox, QSizePolicy, QFrame, \
    QPushButton, QFormLayout, QSpinBox, QSpacerItem, QFileDialog, QTabWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from icecream import ic

from MRISequenceViewer import PlaneViewerQT
from MPRWindow import Ui_MPRWindow
from getMPR import PointsToPlansVectors
from util import config_data, MRI_files

from MainWindowComponents.MessageBoxes import invalidDirectoryMessage, gzipFileMessage, noGoodFiles

ic.configureOutput(includeContext=True)


class Tab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.Tab_Bar = parent
        self.name = "New Tab"
        self.buildNewTab()
        self.oldCoronalIndex = -1 # these are in case image cannot be rendered, return to previous
        self.oldAxialIndex = -1

    def getName(self):
        # returns stylized form of name
        if len(self.name) >= 16:
            return self.name[:16]
        else:
            padding = len(self.name) - 16
            return "{0}{1}{2}".format(' ' * int(padding/2), self.name, ' ' * int((padding/2) + 0.51))

    def _getCommonFont(self) -> QFont:
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        return font

    def _buildCommonLabel(self, cur_label: QLabel, font: QFont, alignment=None) -> QLabel:
        # Shortens process of creating new label with central widget as its parent
        if font is not None:
            cur_label.setFont(font)
        if alignment is not None:
            cur_label.setAlignment(QtCore.Qt.AlignCenter)
        return cur_label

    def buildImageBoundaries(self):
        self.leftLeftBoundary, self.leftRightBoundary, self.rightLeftBoundary, self.rightRightBoundary, self.topBoundary = QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)
        boundaries = [self.leftLeftBoundary, self.leftRightBoundary, self.rightLeftBoundary, self.rightRightBoundary, self.topBoundary]
        for boundary in boundaries:
            self._buildCommonLabel(boundary, self._getCommonFont())
        #self.mainLayout.addWidget(self.topBoundary, 0, 0, 6, 6)
        self.mainLayout.addWidget(self.leftLeftBoundary, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.leftRightBoundary, 1, 2, 1, 1)
        self.mainLayout.addWidget(self.rightLeftBoundary, 1, 4, 1, 1)
        self.mainLayout.addWidget(self.rightRightBoundary, 1, 6, 1, 1)

    def buildSizeSettings(self):
        self.sizeSettingBox = QFormLayout()
        self.windowSizeCaption = QLabel(self.settingsBox)
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
        self.levelSizeButton = QSpinBox(self.settingsBox)
        self.levelSizeButton.setMinimum(-9999)
        self.levelSizeButton.setMaximum(9999)
        self.levelSizeButton.setProperty("value", 800)
        self.levelSizeButton.setObjectName("levelSizeButton")
        self.sizeSettingBox.setWidget(1, QFormLayout.FieldRole, self.levelSizeButton)

    def _buildImageListTitles(self):
        """ builds Axial/Coronal title to scrollable image lists"""
        self.Axiallabel = self._buildCommonLabel(QLabel(), self._getCommonFont())
        self.settingsLayout.addWidget(self.Axiallabel, 1, 0, 1, 1)
        self.Coronallabel = self._buildCommonLabel(QLabel(), self._getCommonFont())
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
        return sizePolicy

    def _addMRIimages(self):
        for i in range(len(self.MRIimages)):
            basename = os.path.basename(self.MRIimages[i])
            basename = basename[:basename.rfind(".")]
            self.AxialImagesList.addItem(basename)
            self.CoronalImagesList.addItem(basename)

    def _buildImageLists(self):
        self.AxialImagesList = QComboBox(self.settingsBox)
        self.AxialImagesList.setSizePolicy(self._buildSizePolicy(self.AxialImagesList))
        self.settingsLayout.addWidget(self.AxialImagesList, 1, 1, 1, 1)
        self.CoronalImagesList = QComboBox(self.settingsBox)
        self.CoronalImagesList.setSizePolicy(self._buildSizePolicy(self.CoronalImagesList))
        self.settingsLayout.addWidget(self.CoronalImagesList, 2, 1, 1, 1)
        self._addMRIimages()


    def buildSettingsLayoutManager(self):
        self.settingsLayout = QGridLayout(self.settingsBox)
        self.settingsLayout.setObjectName("settingsLayout")
        self._buildImageListTitles()  # builds Axial/Coronal title to scrollable image lists
        self._buildSettingsFrame()
        self._buildUpdateButton()
        self._buildImageLists()

    def buildSettingsBox(self):
        self.settingsBox = QGroupBox(self)
        self.settingsBox.showMaximized()
        self.settingsBox.setObjectName("settingsBox")
        self.buildSizeSettings()  # builds the Window and Level size components
        self.buildSettingsLayoutManager()  # builds layout manager for most of the box
        self.settingsLayout.addLayout(self.sizeSettingBox, 5, 1, 1,
                                      1)  # adds box containing Window/level size spin buttons
        self.mainLayout.addWidget(self.settingsBox, 3, 1, 1,
                                  1)  # adds layout containing Setting components to Tab

    def buildUnderBoundaries(self):
        self.pLabel = self._buildCommonLabel(QLabel(), self._getCommonFont(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.pLabel, 2, 5, 1, 1)
        self.iLabel = self._buildCommonLabel(QLabel(), self._getCommonFont(), QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.iLabel, 2, 1, 1, 1)

    def buildCoronalTitle(self):
        self.coronalImageTitle = QLabel(self)
        font = self._getCommonFont()
        self.coronalImageTitle.setFont(font)
        self.coronalImageTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.coronalImageTitle.setObjectName("coronalImageTitle")
        self.mainLayout.addWidget(self.coronalImageTitle, 0, 1, 1, 1)

    def buildCoronalImageFrame(self):
        self.CoronalImageFrame = QGroupBox(self)
        self.CoronalImageFrame.showMaximized()
        self.mainLayout.addWidget(self.CoronalImageFrame, 1, 1, 1, 1)
        self.buildCoronalTitle()  # add S (Coronal) title

    def buildAxialTitle(self):
        self.axialTitle = QtWidgets.QLabel(self)
        font = self._getCommonFont()
        self.coronalImageTitle.setFont(font)
        self.axialTitle.setAutoFillBackground(False)
        self.axialTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.axialTitle, 0, 5, 1, 1)

    def buildAxialImageFrame(self):
        self.axialImageFrame = QGroupBox(self)
        self.axialImageFrame.showMaximized()
        self.buildAxialTitle()
        self.mainLayout.addWidget(self.axialImageFrame, 1, 5, 1, 1)  # ? why is this cut out

    def _buildDivider(self):
        divider = QFrame(self)
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        return divider

    def buildTabDivider(self):
        self.tabDivider = self._buildDivider()
        self.mainLayout.addWidget(self.tabDivider, 1, 1, 2, 2)

    def buildImageDivider(self):
        self.imageDivider = self._buildDivider()
        self.mainLayout.addWidget(self.imageDivider, 1, 3, 1, 1)

    def buildDividers(self):
        self.buildTabDivider()
        self.buildImageDivider()

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
        self.lengthAnswerTag.setObjectName("lengthAnswerTag")
        self.actionsLayout.addWidget(self.lengthAnswerTag, 8, 2, 1, 1)
        self.addSpacers()

    def buildDotCalculatingBox(self):
        self.dotCalculatingBox = QGroupBox(self)
        self.dotCalculatingBox.setTitle("")
        self.dotCalculatingBox.setObjectName("dotCalculatingBox")
        self.buildActionsBox()
        self.mainLayout.addWidget(self.dotCalculatingBox, 3, 5, 1, 1)


    def retranslateUi(self, Tab):
        _translate = QCoreApplication.translate
        Tab.setWindowTitle(_translate("Tab", "Tab"))
        # set text to widgets in the center near the images
        self.coronalImageTitle.setText(_translate("Tab", "S (Coronal)"))
        self.axialTitle.setText(_translate("Tab", "A (Axial)"))
        self.rightLeftBoundary.setText(_translate("Tab", "R"))
        self.rightRightBoundary.setText(_translate("Tab", "L"))
        self.leftLeftBoundary.setText(_translate("Tab", "L"))
        self.leftRightBoundary.setText(_translate("Tab", "R"))
        self.pLabel.setText(_translate("Tab", "P"))
        self.iLabel.setText(_translate("Tab", "I"))
        # set text to widgets in the settings box
        self.settingsBox.setTitle(_translate("Tab", "Settings"))
        self.Axiallabel.setText(_translate("Tab", "Axial"))
        self.Coronallabel.setText(_translate("Tab", "Coronal"))
        self.levelSizeCaption.setText(_translate("Tab", "Level"))
        self.windowSizeCaption.setText(_translate("Tab", "Window"))
        self.updateButton.setText(_translate("Tab", "Update"))
        # set text to widgets in actions box
        # self.putMPRDotsButton.setText(_translate("Tab", "Set Points - Calculate MPR"))
        # self.calcLengthButton.setText(_translate("Tab", "Calculate Length"))
        # self.putLengthDotsButton.setText(_translate("Tab", "Set Points - Calculate Length"))
        # set text to widgets in Menu bar

    # def updateWindow
    def WindowLevelUpdate(self):
        self.AxialViewer.adjustWindow(self.windowSizeButton.value())
        self.AxialViewer.adjustLevel(self.levelSizeButton.value())
        self.AxialViewer.updateWindowLevelLabels()
        self.CoronalViewer.adjustWindow(self.windowSizeButton.value())
        self.CoronalViewer.adjustLevel(self.levelSizeButton.value())
        self.CoronalViewer.updateWindowLevelLabels()

    def pickMPRpointsStatus(self):
        if self.CoronalViewer.interactorStyle.actions["PickingMPR"] == 0:
            self.CoronalViewer.interactorStyle.actions["PickingMPR"] = 1
            self.putMPRDotsButton.setStyleSheet("QPushButton { background-color: rgb(255, 255, 255); }")
        else:
            self.CoronalViewer.interactorStyle.actions["PickingMPR"] = 0
            self.putMPRDotsButton.setStyleSheet("QPushButton { background-color: rgb(255, 255, 255); }")

    def pickLengthPointsStatus(self):
        # print("PushButten clicked")
        if self.CoronalViewer.interactorStyle.actions["PickingLength"] == 0:
            self.CoronalViewer.interactorStyle.actions["PickingLength"] = 1
            self.putLengthDotsButton.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.CoronalViewer.interactorStyle.actions["PickingLength"] = 0
            self.putLengthDotsButton.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")

    def openMPRWindow(self, MPR_M, delta, MPRposition, ListOfPoints, ViewMode):
        self.window = QTabWidget()
        self.ui = Ui_MPRWindow()
        self.ui.setupUi(self.window, MPR_M, delta, MPRposition, self.ViewerProperties, ListOfPoints, ViewMode)
        self.window.show()

    def calculateMPR(self):
        points = self.CoronalViewer.mprPoints.pointCoordinatesAsList
        ViewMode = 'Coronal'
        ic(points)
        GetMPR = PointsToPlansVectors(self.ViewerProperties, points, ViewMode, Plot=False, height=40, viewAngle=180)
        MPR_M = GetMPR.MPR_M
        delta = GetMPR.delta
        MPRposition = GetMPR.MPR_indexs_np
        self.openMPRWindow(MPR_M, delta, MPRposition, points, ViewMode)

    def pickleDistances(self, DistancePickingIndexs, allDistances):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.settingsBox, "QFileDialog.getSaveFileName()", "",
                                                  options=options)
        print(fileName)
        if fileName != "":
            outfile = open(fileName, 'wb')
            pickle.dump([DistancePickingIndexs, allDistances], outfile)
            outfile.close()

    def calculateDistances(self):
        """ Calculates distances between set points and outputs reselt to GUI"""
        DistancePickingIndexs = self.CoronalViewer.lengthPoints.points
        DistancePickingIndexs = np.asarray(DistancePickingIndexs)
        allDistances = [np.linalg.norm(DistancePickingIndexs[j + 1, 0:3] - DistancePickingIndexs[j, 0:3]) for j in
                        range(len(DistancePickingIndexs) - 1)]
        allDistances = np.asarray(allDistances)
        totalDistance = np.sum(allDistances)
        strDistances = ["{0:.2f}".format(allDistances[i]) for i in range(len(allDistances))]
        self.lengthAnswerTag.setText(
            "The lengths [mm] are: {0} \n\nThe total length: {1}".format(' , '.join(strDistances),
                                                                         "{0:.2f}".format(totalDistance)))
        self.lengthAnswerTag.adjustSize()
        self.pickleDistances(DistancePickingIndexs, allDistances)

    def connectAllButtons(self):
        self.updateButton.clicked.connect(lambda: self.loadImageViewers())
        self.windowSizeButton.valueChanged.connect(lambda: self.WindowLevelUpdate())
        self.levelSizeButton.valueChanged.connect(lambda: self.WindowLevelUpdate())
        # self.putMPRDotsButton.clicked.connect(lambda: self.pickMPRpointsStatus())
        # self.putLengthDotsButton.clicked.connect(lambda: self.pickLengthPointsStatus())
        # self.calcMPRButton.clicked.connect(lambda: self.calculateMPR())
        # self.calcLengthButton.clicked.connect(lambda: self.calculateDistances())

    def setWindowValues(self):
        self.windowSizeButton.setValue(self.CoronalViewer.WindowVal)
        self.levelSizeButton.setValue(self.CoronalViewer.LevelVal)

    def loadImages(self):
        fileExplorer = QFileDialog(
            directory=config_data.get_config_value("DefaultFolder"))  # opens location to default location
        folderPath = str(fileExplorer.getExistingDirectory())
        self.MRIimages = MRI_files.getMRIimages(folderPath) # so can be loaded by the viewers
        # this must be set after MRIimages or else tab will be renamed to blank if user X-es out file explorer since error is thrown there
        self.name = folderPath[folderPath.rfind(os.path.sep) + 1:]

    def clearDefault(self):
        self.mainLayout.removeWidget(self.defaultTabMainWidget)
        sip.delete(self.defaultTabMainWidget)
        self.defaultTabMainWidget = None

    def loadRegularTab(self):
        try:
            self.loadImages()
        except FileNotFoundError: # user X-ed out file explorer
            return -1
        if len(self.MRIimages) < 1:  # open file explorer and load selected NRRD images
            invalidDirectoryMessage()
            return -1
        self.Tab_Bar.change_tab_name(self)
        self.clearDefault()
        self.buildSettingsBox()  # builds components for 'settings' in the bottom left
        self.buildCoronalImageFrame()  # builds frame containing coronal image
        self.buildAxialImageFrame()  # builds frame containing axial image
        self.loadImageViewers()  # load viewer for scan images
        self.setWindowValues()  # set window size values based on opening
        self.connectAllButtons()  # connect all buttons to the functions called when they are clicked, updated
        self.buildImageBoundaries()  # Sets L/R marking on sides of NRRM images


        self.buildDividers()  # creates line seperating axial and coronal images
        self.buildUnderBoundaries()  # builds P and I captions to image frames
        self.retranslateUi(self)  # adds text to all widgets
        QMetaObject.connectSlotsByName(self)  # connect all components to Tab
        # self.buildDotCalculatingBox()  # builds box containing buttons for dot-putting calculations

    def show_valid_image(self, currentAxialIndex, currentCoronalIndex):
        if self.oldCoronalIndex == -1: # first image is being loaded
            if currentAxialIndex == len(self.MRIimages)-1:
                noGoodFiles()
            else:
                self.CoronalImagesList.setCurrentIndex(currentCoronalIndex+1)
                self.AxialImagesList.setCurrentIndex(currentAxialIndex+1)
                self.loadImageViewers()
        else:
            if currentCoronalIndex != self.oldCoronalIndex:
                self.CoronalImagesList.setCurrentIndex(self.oldCoronalIndex)
            if currentAxialIndex != self.oldAxialIndex:
                self.AxialImagesList.setCurrentIndex(self.oldAxialIndex)
            gzipFileMessage()
            self.loadImageViewers()

    def rememberIndices(self, axialIndex: int, coronalIndex: int):
        self.oldAxialIndex = axialIndex
        self.oldCoronalIndex = coronalIndex

    def loadImageViewers(self):
        AxialVTKQidget = QVTKRenderWindowInteractor(self.axialImageFrame)
        self.mainLayout.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        CoronalVTKQidget = QVTKRenderWindowInteractor(self.CoronalImageFrame)
        self.mainLayout.addWidget(CoronalVTKQidget, 1, 1, 1, 1)

        try:
            self.AxialViewer = PlaneViewerQT(AxialVTKQidget, self.MRIimages[int(self.AxialImagesList.currentIndex())],
                                             'Axial', self.MRIimages[0][-4:] != "nrrd")
            self.CoronalViewer = PlaneViewerQT(CoronalVTKQidget, self.MRIimages[int(self.CoronalImagesList.currentIndex())],
                                             'Coronal', self.MRIimages[0][-4:] != "nrrd")

        except AttributeError: # GZIP, unreadable file picked
            self.show_valid_image(int(self.AxialImagesList.currentIndex()), int(self.CoronalImagesList.currentIndex())) # show any valid MRI image instead of improper image and show Error

        self.rememberIndices(int(self.AxialImagesList.currentIndex()), int(self.CoronalImagesList.currentIndex())) # remember that these indices worked


    def setTabColor(self):
        self.setStyleSheet("background-color: rgb(68, 71, 79);\n"
                                 "border-color: rgb(0, 0, 0);")

    def buildMainLayoutManager(self):
        self.mainLayout = QGridLayout(self)

    def buildDefaultTab(self) -> QWidget:
        self.defaultTabMainWidget = QWidget()
        addFilesButton = QPushButton(self.defaultTabMainWidget)
        addFilesButton.setText(QCoreApplication.translate("Tab", "Add MRI Images"))
        addFilesButton.setGeometry(QRect(375, 290, 960, 231)) #EMPHASIS# should be made more portable
        addFilesButton.clicked.connect(self.loadRegularTab) # loads MRI viewer
        self.mainLayout.addWidget(self.defaultTabMainWidget)

    def buildNewTab(self):
        self.setTabColor()
        self.buildMainLayoutManager()
        self.buildDefaultTab() # builds default tab until user adds regular MRI files


