import numpy as np
from typing import List
from Model.getMPR import PointsToPlaneVectors


class MPRW_Control:
    def __init__(self, allPoints: List[np.array], imageData):
        self.points = allPoints
        self.image_data = imageData
        self.height = 40
        self.viewAngle = 180

    def calculate(self):
        _mpr_properties = PointsToPlaneVectors(self.points, self.image_data, Plot=0,
                                               height=self.height, viewAngle=self.viewAngle)
        return _mpr_properties

    def __repr__(self):
        return str(f'height: {self.height}, angle: {self.viewAngle}')
