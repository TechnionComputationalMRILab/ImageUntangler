

class viewerLogic:
    def __init__(self, MPR_M, delta, MPRposition, ListOfPoints, Height, angle):
        self.MPR_M = MPR_M
        self.delta = delta
        self.originalPoints = ListOfPoints
        self.Height = Height
        self.angle = angle
        self.MPRposition = MPRposition
        self.DistancePickingIndexs =[]

        self.ConvViewerProperties = None
        self.ConvViewMode = None



