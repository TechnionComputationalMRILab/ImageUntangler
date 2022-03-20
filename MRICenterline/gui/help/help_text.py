class HelpText:
    text_array = []
    text_length = len(text_array)
    text_color = (1, 0, 0)
    text_out = "{}".format("\n".join(text_array))


class InteractorHelpText(HelpText):
    text_array = ["HELP",
                  'c: toggle cursor',
                  "h: toggle this help text",
                  'Up/Down: change slice index',
                  'Right-click + drag: zoom',
                  'Middle-click + drag: pan']
