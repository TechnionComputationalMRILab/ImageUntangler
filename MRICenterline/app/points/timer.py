from MRICenterline.app.points.status import TimerStatus


class Timer:
    status = TimerStatus.STOPPED

    def __init__(self):
        pass

    def calculate_time_gap(self):
        return 0.0