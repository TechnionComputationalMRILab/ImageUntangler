

class viewerLogic:
    def __init__(self, MPR_M, delta, MPRposition, ListOfPoints, Height, angle, ConvViewerProperties, ConvViewMode):
        self.MPR_M = MPR_M
        self.delta = delta
        self.originalPoints = ListOfPoints
        self.Height = Height
        self.angle = angle
        self.ConvViewerProperties = ConvViewerProperties
        self.ConvViewMode = ConvViewMode
        self.MPRposition = MPRposition
        self.DistancePickingIndexs =[]
        self.window =  self.ConvViewerProperties.WindowVal
        self.level = self.ConvViewerProperties.LevelVal




