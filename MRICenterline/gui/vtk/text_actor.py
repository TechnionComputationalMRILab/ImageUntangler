from vtkmodules.all import vtkTextActor

from MRICenterline import CFG


class IUTextActor(vtkTextActor):
    def __init__(self, input_text: str = " ", visibility: bool = True, position: int = -1, color=None):
        super().__init__()

        font_size = int(CFG.get_config_data('display', 'font-size'))
        if not color:
            color = CFG.get_color('display', 'text-color')

        self.GetTextProperty().SetFontSize(font_size)
        self.GetTextProperty().SetColor(*color)
        self.SetInput(input_text)
        self.SetVisibility(visibility)

        if position >= 0:
            self.SetDisplayPosition(0, position * font_size)

    def change_text(self, input_text: str):
        self.SetInput(input_text)

    def change_visibility(self, visibility: bool):
        self.SetVisibility(visibility)
