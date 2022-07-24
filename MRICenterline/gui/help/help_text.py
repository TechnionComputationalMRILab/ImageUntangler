from MRICenterline import CFG


class InteractorHelpText:
    text_array = ["HELP",
                  'c: toggle cursor',
                  "h: toggle this help text",
                  'Up/Down: change slice index',
                  'Right-click + drag: zoom',
                  'Middle-click + drag: pan']
    text_length = len(text_array)
    text_color = CFG.get_color('display', 'help-text-color')
    text_out = "{}".format("\n".join(text_array))


class CenterlineInteractorHelpText:
    text_array = ["HELP",
                  'Middle scroll wheel: change angle',
                  "Shift + Middle scroll wheel: change height"]
    text_length = len(text_array)
    text_color = CFG.get_color('display', 'help-text-color')
    text_out = "{}".format("\n".join(text_array))
