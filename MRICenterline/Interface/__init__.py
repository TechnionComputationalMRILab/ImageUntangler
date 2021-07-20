from MRICenterline.Points.PointCollection import PointCollection

import logging
logging.getLogger(__name__)


class DisplayCenterlineInterface:
    def __init__(self):
        self.level = 0
        self.window = 0
        self.points = PointCollection()
        self.updated = False

    def initialize_level_window(self, level, window):
        self.level = level
        self.window = window

    def initialize_points(self, points):
        self.points = points

    def set_level(self, level):
        self.level = level
        self.updated = True

    def set_window(self, window):
        self.window = window
        self.updated = True

    def set_points(self, points):
        self.points = points
        self.updated = True

    def __repr__(self):
        return str({"level": self.level,
                "window": self.window,
                "number of points": len(self.points)})
