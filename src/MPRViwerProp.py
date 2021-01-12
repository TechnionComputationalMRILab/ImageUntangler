

class viewerLogic:
    def __init__(self,MPR_M,delta,MPRPosiotion,ListOfPoints,Height,angle, ConvViewerProperties, ConvViewMode):
        self.MPR_M = MPR_M
        self.delta = delta
        self.ListOfPoints_Original = ListOfPoints
        self.Height = Height
        self.angle = angle
        self.ConvViewerProperties = ConvViewerProperties
        self.ConvViewMode = ConvViewMode
        self.MPRPosiotion = MPRPosiotion
        self.DistancePickingIndexs =[]
        self.DisCalculate = []
        self.PointsForDisCalPosition = []
        self.window =  self.ConvViewerProperties.WindowVal
        self.level = self.ConvViewerProperties.LevelVal
        # self.window = self.MPR_M.max()-self.MPR_M.min()
        # self.level = (self.MPR_M.max()+self.MPR_M.min())/2



