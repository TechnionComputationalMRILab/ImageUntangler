def height_minmax():
    """
    Limits the values in the set height spinbox.
    Entering a value too large will make the program crash, so limiting it here is important
    """
    return 0, 150


def angle_minmax():
    """
    Mostly implemented for the sake of similarity with height_minmax...
    """
    return 0, 180


def default_initial_angle():
    return 180


def default_initial_height():
    return 40
