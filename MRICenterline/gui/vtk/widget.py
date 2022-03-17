from PyQt5.Qt import QSizePolicy
from PyQt5.QtWidgets import QWidget, QVBoxLayout

import vtkmodules.all as vtk


class IUVTKWidget(QWidget):
    def __init__(self, model, interactor, interactor_style, parent_widget=None):
        super().__init__(parent_widget)
        layout = QVBoxLayout(self)
        self.model = model
        self.interactor = interactor
        self.interactor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.interactor_style = interactor_style

        layout.addWidget(self.interactor)

        self.ren = vtk.vtkRenderer()
        self.interactor.GetRenderWindow().AddRenderer(self.ren)
        self.window = self.interactor.GetRenderWindow()

        self.iren = self.interactor.GetRenderWindow().GetInteractor()
        self.ren.ResetCamera()

        # Create an actor
        self.actor = vtk.vtkImageActor()
        self.ren.AddActor(self.actor)
        self.configure_actor()

        self.interactor.SetInteractorStyle(self.interactor_style)
        self.window.SetInteractor(self.interactor)

        self.configure_camera()

        self.window.Render()

        # interactorStyle.AddObserver("KeyPressEvent", self.KeyPressCallback)
        # interactorStyle.AddObserver("LeftButtonPressEvent", self.LeftButtonDownCallback)

        self.show()

    def show(self):
        self.iren.Initialize()
        self.iren.Start()
        # super().show()

    def configure_actor(self):
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        self.actor.SetMapper(mapper)

    def configure_camera(self):
        pass
