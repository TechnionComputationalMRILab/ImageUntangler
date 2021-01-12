# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MPRWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import getMPR
import MPRViewer
import MPRViwerProp
import pickle


class Ui_MPRWindow:
    def setupUi(self, MPRWindow, MPR_M, delta, MPRPosiotion, ConvViewerProperties, ListOfPoints, ConvViewMode):



        MPRWindow.setObjectName("MainWindow")
        MPRWindow.resize(990, 797)
        MPRWindow.setMaximumSize(QtCore.QSize(990, 16777215))
        self.centralwidget = QtWidgets.QWidget(MPRWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SetPoints = QtWidgets.QPushButton(self.groupBox_3)
        self.SetPoints.setObjectName("SetPoints")
        self.verticalLayout.addWidget(self.SetPoints, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.groupBox_2, 1, 2, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox.setMaximum(5000.0)
        self.doubleSpinBox.setProperty("value", 20.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.updateButton = QtWidgets.QPushButton(self.groupBox_4)
        self.updateButton.setObjectName("updateButton")
        self.gridLayout_2.addWidget(self.updateButton, 2, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox.setMaximum(180)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setRowStretch(0, 4)
        self.gridLayout.setRowStretch(1, 1)
        MPRWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MPRWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 990, 22))
        self.menubar.setObjectName("menubar")
        MPRWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MPRWindow)
        self.statusbar.setObjectName("statusbar")
        MPRWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MPRWindow)
        QtCore.QMetaObject.connectSlotsByName(MPRWindow)


        # self.Visualize_MPR(MPR_M,delta)


        Height = self.doubleSpinBox.value()
        angle = self.spinBox.value()

        self.LoadViewer(MPR_M, delta,MPRPosiotion, ListOfPoints, ConvViewerProperties,Height, angle,ConvViewMode)


        # self.doubleSpinBox.valueChanged.connect(lambda: self.HeigthChanged())
        self.updateButton.clicked.connect(lambda: self.HeigthChanged())
        self.pushButton.clicked.connect(lambda: self.SaveFile())
        self.SetPoints.clicked.connect(lambda: self.SetPointsClick())
        self.pushButton_2.clicked.connect(lambda: self.CalculateDis())



    def LoadViewer(self, MPR_M, delta,MPRPosiotion, ListOfPoints, ConvViewerProperties, Height, angle,ConvViewMode):

        # self.ViewerProperties = ViewerProp.viewerLogic(self.FolderPath,str(self.UpLowBox.currentText()),str(self.AxialSeqBox.currentText()),
        #                                                str(self.CoronalSeqBox.currentText()), self.spinBoxWindow.value(), self.spinBoxLevel.value())

        # AxialVTKQidget = QVTKRenderWindowInteractor(self.groupBox)
        # self.gridLayout_3.addWidget(AxialVTKQidget, 1, 5, 1, 1)
        # self.AxialViewer = AxialCoronalViewer.PlaneViewerQT(AxialVTKQidget, self.ViewerProperties, 'Axial')
        self.MPRViewerProperties = MPRViwerProp.viewerLogic(MPR_M, delta,MPRPosiotion, ListOfPoints, Height, angle, ConvViewerProperties, ConvViewMode)


        self.interactor = QVTKRenderWindowInteractor(self.groupBox)
        self.gridLayout.addWidget(self.interactor, 0, 0, 1, 3)
        self.MPR_Viewer = MPRViewer.View(self.interactor,self.MPRViewerProperties)


    def HeigthChanged(self):
        self.MPRViewerProperties.MPRHeight = self.doubleSpinBox.value()
        self.MPRViewerProperties.Angle = self.spinBox.value()
        plot = 0
        self.GetMPR = getMPR.PointsToPlansVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.ListOfPoints_Original, self.MPRViewerProperties.ConvViewMode, Height=self.MPRViewerProperties.MPRHeight,
                                             viewAngle=self.MPRViewerProperties.Angle, Plot=plot)
        self.MPRViewerProperties.MPR_M = self.GetMPR.MPR_M
        self.MPRViewerProperties.delta = self.GetMPR.delta
        self.MPRViewerProperties.MPRPosiotion = self.GetMPR.MPR_indexs_np
        self.MPR_Viewer.Visualize_MPR()

    # def AngleChangeByIneractor(self,angle):
    #     self.Hegith = self.doubleSpinBox.value()
    #     self.Angle = angle
    #     plot = 0
    #     GetMPR = getMPR.PointsToPlansVectors(self.ViewerProperties, self.ListOfPoints, self.ViewMode, Heigth=self.Hegith,
    #                                          viewAngle=self.Angle, Plot=plot)
    #     MPR_M = GetMPR.MPR_M
    #     delta = GetMPR.delta
    #     self.spinBox.setValue(angle)
    #     self.MPR_Viewer.Visualize_MPR(MPR_M, delta)


    def SetPointsClick(self):
        if self.MPR_Viewer.interactorStyle.actions["Picking"] == 0:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 1
            self.SetPoints.setStyleSheet("QPushButton { background-color: rgb(0,76,153); }")
        else:
            self.MPR_Viewer.interactorStyle.actions["Picking"] = 0
            self.SetPoints.setStyleSheet("QPushButton { background-color: rgb(171, 216, 255); }")
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
        self.label_2.setText("The lengths [mm] are:\n\n {0} \n\nThe total length:\n\n {1}".format(' , '.join(strdis),"{0:.2f}".format(TotlalD)))
        # self.GetMPR.PlotSelectedPointsForDis(Points_Position)
        self.label_2.adjustSize()

    def SaveFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.groupBox, "QFileDialog.getSaveFileName()", "", options=options)
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
        self.groupBox_3.setTitle(_translate("MainWindow", "Calculate Distance"))
        self.SetPoints.setText(_translate("MainWindow", "Set Points"))
        self.pushButton_2.setText(_translate("MainWindow", "Calculate Length"))
        self.pushButton.setText(_translate("MainWindow", "Save"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Result"))
        # self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.groupBox_4.setTitle(_translate("MainWindow", "GroupBox"))
        self.label_3.setText(_translate("MainWindow", "Angle"))
        self.label.setText(_translate("MainWindow", "Height"))
        self.label_4.setText(_translate("MainWindow", "[mm]"))
        self.label_5.setText(_translate("MainWindow", "deg"))
        self.updateButton.setText(_translate("MainWindow", "Update"))
        self.groupBox.setTitle(_translate("MainWindow", "MPR"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MPRWindow = QtWidgets.QMainWindow()
    ui = Ui_MPRWindow()
    ui.setupUi(MPRWindow)
    MPRWindow.show()
    sys.exit(app.exec_())
