import sys
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
from icecream import ic
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk


class MainWindow(Qt.QMainWindow):

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(1,1,1)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()

    def add_actor(self, actor):
        self.ren.AddActor(actor)

    def start(self):
        self.ren.ResetCamera()

        self.iren.Initialize()
        self.iren.Start()


if __name__ == "__main__":
    from MRICenterline.Points.PointArray import PointArray

    pa = PointArray()
    pa.add_point([0, 5, 0])
    pa.add_point([-1, 1.5, 0])
    pa.add_point([1, 0, 0])
    pa.add_point([0, 2, 0])

    pa.set_color((1,0.5,0))

    app = Qt.QApplication(sys.argv)
    window = MainWindow()

    for i in pa.get_actor_list():
        window.add_actor(i)

    # for i in pa.show_length_text_actors():
    #     window.add_actor(i)

    # window.add_actor(pa.get_line_actor())
    #
    # ic(pa.lengths)

    window.start()
    sys.exit(app.exec_())
