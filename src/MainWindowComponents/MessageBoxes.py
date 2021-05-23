from PyQt5.QtWidgets import QMessageBox
from util import stylesheets


def invalidDirectoryMessage():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("Invalid Directory")
    errorMessage.setText("Selected Directory has No MRI Images")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.exec_()


def gzipFileMessage():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("GZIP File")
    errorMessage.setText("Selected File has GZIP Encoding, Which VTK NRRD Reader Cannot Handle")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.setDetailedText("ERROR: In /work/standalone-x64-build/VTK-source/IO/Image/vtkNrrdReader.cxx\n"
                                 "vtkNrrdReader: Unsupported encoding: gzip\n"
                                 "ERROR: In /work/standalone-x64-build/VTK-source/Common/ExecutionModel/vtkExecutive.cxx\n"
                                 "vtkCompositeDataPipeline: Algorithm vtkNrrdReader returned failure for request: vtkInformation")
    errorMessage.exec_()


def noGoodFiles():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("All Files Unreadable")
    errorMessage.setText("All Selected Files are Unreadable because they are GZIP Encoded. Please Open a New Tab and Try Again")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.setDetailedText("All files Caused the Following Error: \n"
                                  "ERROR: In /work/standalone-x64-build/VTK-source/IO/Image/vtkNrrdReader.cxx\n"
                                 "vtkNrrdReader: Unsupported encoding: gzip\n"
                                 "ERROR: In /work/standalone-x64-build/VTK-source/Common/ExecutionModel/vtkExecutive.cxx\n"
                                 "vtkCompositeDataPipeline: Algorithm vtkNrrdReader returned failure for request: vtkInformation")
    errorMessage.exec_()


def notEnoughPointsClicked(function):
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("Not Enough Points")
    errorMessage.setText(f"Not enough points clicked to calculate {function}!")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.exec_()


def file_mismatch_warning():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("File mismatch")
    errorMessage.setText(f"Filename in loaded JSON file does not match currently opened sequence")
    errorMessage.setIcon(QMessageBox.Warning)
    errorMessage.exec_()


def json_file_wrong_headers():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet(stylesheets.get_sheet_by_name("ErrorMessage"))
    errorMessage.setWindowTitle("JSON file invalid")
    errorMessage.setText(f"Invalid JSON file opened")
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.exec_()