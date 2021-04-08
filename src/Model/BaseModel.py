from typing import List, Tuple
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QMainWindow

from MPRwindow.MPRWindow import Ui_MPRWindow

from util import stylesheets
from View.SlidersLayout import SlidersLayout
from View.Toolbar import Toolbar
from Model.NRRDViewerManager import NRRDViewerManager
from Model.getMPR import PointsToPlaneVectors
from Control.SequenceInteractorWidgets import SequenceInteractorWidgets
from Control.SequenceViewerInteractorStyle import SequenceViewerInteractorStyle
from MPRWindow2.MPRWindow import MPRWindow, CustomDialog
from MPRWindow2.Control.MPRW_Control import MPRW_Control
from MPRWindow2.Model.MPRW_Model import MPRW_Model

from MPRWindow2.MPRWindow import MPRWindow
from MPRWindow2.MPRW_Control import MPRW_Control

class BaseModel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.toolbar = Toolbar(parent=self, manager=self)
        self.toolbar.setGeometry(QRect(0, 0, 500, 22))
        #self.interactor = QVTKRenderWindowInteractor(frame)
        self.pickingLengthPoints = False
        self.pickingMPRpoints = False
        #------------------------------
        """
        self.interactorStyle = SequenceViewerInteractorStyle(parent=self.interactor, model=self)
        self.widgets = SequenceInteractorWidgets(MRIimages, self)
        self.sequenceManager = ViewerManager(self,  MRIimages)
        self.view = self.sequenceManager.loadSequence(0, self.interactor, self.interactorStyle)
        slidersLayout = SlidersLayout(sequenceList=self.widgets.sequenceList,  windowSlider=self.widgets.windowSlider,
                                      levelSlider=self.widgets.levelSlider, indexSlider=self.widgets.indexSlider)
        self.initializeSliderValues()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.interactor)
        self.layout.addLayout(slidersLayout)
        """
#_________________________________________Constructor functions_____________________________________


#_________________________________________Constructor functions_____________________________________
    @staticmethod
    def buildFrame():
        frame = QGroupBox()
        frame.showMaximized()
        return frame

#_____________________________________________Interface to Widgets______________________________________________________________

    def changeSequence(self, sequenceIndex: int):
        raise NotImplementedError

    def setListWidgetIndex(self, index):
        # sets index of sequences in list of sequences; used in case of illegitimate selected file
        self.widgets.sequenceList.setCurrentIndex(index)

    def changeWindow(self, window: int):
        self.widgets.windowSlider.setValue(window)
        self.view.adjustWindow(window)

    def changeLevel(self, level: int):
        self.widgets.levelSlider.setValue(level)
        self.view.adjustLevel(level)

    def setIndex(self, index: int):
        raise NotImplementedError

    def updateSliderIndex(self, index):
        self.widgets.indexSlider.setValue(index)

    #__________________________________________ Interface to InteractorStyle ________________________________

    def moveBullsEye(self, coordinates: Tuple[int]):
        self.view.moveBullsEye(coordinates)

    def updateWindowLevel(self):
        self.view.updateWindowLevel()

    def updateZoomFactor(self):
        self.view.updateZoomFactor()

    def clearCursor(self):
        self.view.Cursor.AllOff()
        self.view.window.Render()

    def addCursor(self):
        self.view.Cursor.AllOff()
        self.view.Cursor.AxesOn()
        self.view.window.Render()

    def changeSliceIndex(self, changeFactor: int):
        raise NotImplementedError

    def addPoint(self, pointType: str, pickedCoordinates: Tuple[int]):
        self.view.addPoint(pointType, pickedCoordinates)

#________________________________________Interface to Toolbar_____________________________________
    def reverseMPRpointsStatus(self):
        self.interactorStyle.actions["PickingMPR"] = int(not self.interactorStyle.actions["PickingMPR"])

    def reverseLengthPointsStatus(self):
        self.interactorStyle.actions["PickingLength"] = int(not self.interactorStyle.actions["PickingLength"])

    def calculateLengths(self):
        pass

    def calculateMPR(self):
        # TODO
        MPRproperties = PointsToPlaneVectors(self.view.MPRpoints.getCoordinatesArray(), self.view.imageData, Plot=0, height=40, viewAngle=180)
        MPR_M = MPRproperties.MPR_M
        delta = MPRproperties.delta
        MPRposition = MPRproperties.MPR_indexs_np
        self.openMPRWindow(MPR_M, delta, MPRposition, self.view.MPRpoints.getCoordinatesArray())

    def openMPRWindow(self, MPR_M, delta, MPRposition, points):
        print("attempting to open mpr window")
        # _control = MPRW_Control(MPR_M, delta, MPRposition, points)
        # # _dialog_box = MPRWindow(_control)
        # _dialog_box = CustomDialog()
        # _dialog_box.show()
        #
        # window = QMainWindow()
        # ui = Ui_MPRWindow()
        # ui.setupUi(window, MPR_M, delta, MPRposition, points)
        # window.setStyleSheet(stylesheets.get_sheet_by_name("Default"))
        # window.show()
        #
        # _points = self.view.MPRpoints.getCoordinatesArray()
        # _image_data = self.view.imageData
        #
        # _control = MPRW_Control(_points, _image_data)
        #
        # _dlg = MPRWindow()
        # _dlg.set_control(_control)
        # ic(_dlg)
        # _dlg.open_()
