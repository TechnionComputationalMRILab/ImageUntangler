

class MPRW_Control:
    def __init__(self, MPR_M, delta, MPRposition, points):
        self.MPR_M = MPR_M
        self.delta = delta
        self.MPRposition = MPRposition
        self.originalPoints = points
        self.DistancePickingIndexs = []
        self.window = 0
        self.level = 0

    def set_height(self, height):
        self.height = height

    def set_angle(self, angle):
        self.angle = angle
