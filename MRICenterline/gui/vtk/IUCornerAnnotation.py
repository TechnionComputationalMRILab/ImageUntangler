from typing import Dict
from enum import Enum
from vtkmodules.all import vtkCornerAnnotation


class CornerLoc(Enum):
    LOWER_LEFT = 0
    LOWER_RIGHT = 1
    UPPER_LEFT = 2
    UPPER_RIGHT = 3


class IUCornerAnnotation(vtkCornerAnnotation):
    def __init__(self, location: CornerLoc, color=(0, 0, 0), font_size: int = 30):
        super().__init__()
        self.int_loc = location.value
        self.is_visible = True
        self.text = ""

        self.GetTextProperty().SetColor(color)
        self.SetLinearFontScaleFactor(2)
        self.SetNonlinearFontScaleFactor(1)
        self.SetMaximumFontSize(font_size)

    def SetInput(self, string: str or Dict[str]):
        if type(string) is str:
            self.text = string

        elif type(string) is dict:
            vals = [f'{str(key)}: {str(val)}' for key, val in string.items()]
            self.text = "{}".format("\n".join(vals))

        self.SetText(self.int_loc, self.text)

    def SetVisibility(self, show):
        self.is_visible = show

        if self.is_visible:
            self.SetText(self.int_loc, self.text)
        else:
            self.SetText(self.int_loc, "")

    def SetColor(self, color):
        self.GetTextProperty().SetColor(color)
