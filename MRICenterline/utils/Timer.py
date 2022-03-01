from datetime import datetime, timezone, timedelta
from enum import Enum

import logging
logging.getLogger(__name__)


class Timer:
    """ Basic stopwatch with pause/resume functionality """
    def __init__(self):
        self._status = None
        self._start_time = None
        self._stop_time = None
        self._resume_time = None
        self._pause_time = None
        self._time_gap = []

    def start_timer(self) -> None:
        self._status = TimerStatus.START

        self._start_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Starting timer: {self._start_time}")

    def stop_timer(self) -> None:
        # if the _status is paused, resume it so that the time gap will be recorded
        if self._status == TimerStatus.PAUSED:
            self.resume_timer()

        self._status = TimerStatus.STOP

        self._stop_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Stopping timer: {self._stop_time}")

    def pause_timer(self) -> None:
        self._status = TimerStatus.PAUSED

        self._pause_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Pausing timer: {self._pause_time}")

    def resume_timer(self) -> None:
        self._status = TimerStatus.RESUMED

        self._resume_time = datetime.now(timezone.utc).astimezone()
        logging.info(f"Resuming timer: {self._resume_time}")

        logging.info(f"Time gap: {self._resume_time - self._pause_time}")
        self._time_gap.append(self._resume_time - self._pause_time)

    def get_total_time_elapsed(self) -> int:
        if self._status is None:
            return 0

        if self._status is TimerStatus.STOP:

            if self._time_gap:
                measured_time = self._stop_time - self._start_time - sum(self._time_gap, timedelta())
            else:
                measured_time = self._stop_time - self._start_time

            logging.info(f"Time measured: {measured_time.total_seconds()}")
            return int(measured_time.total_seconds())
        else:
            self.stop_timer()
            self.get_total_time_elapsed()


class TimerStatus(Enum):
    START = 1
    STOP = 0
    PAUSED = -1
    RESUMED = 2


if __name__ == "__main__":
    import time
    import random
    test_num = 5

    # basic start-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start_timer()
        pause = random.randrange(0, 10)
        print("sleeping for", pause, "seconds", end=" | ")
        time.sleep(pause)
        timer.stop_timer()
        time_elapsed = timer.get_total_time_elapsed()
        print("timer measured", time_elapsed)
        assert pause == time_elapsed
    else:
        print('Basic test done')

    # start-(pause/resume)-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start_timer()

        # let timer run for some time
        run_time = random.randrange(0, 10)
        print("sleeping for", run_time, "seconds", end=" | ")
        time.sleep(run_time)

        timer.pause_timer()

        # pause the timer
        paused_time = random.randrange(0, 10)
        print("sleeping for", paused_time, "seconds", end=" | ")
        time.sleep(paused_time)

        timer.resume_timer()

        timer.stop_timer()
        time_elapsed = timer.get_total_time_elapsed()
        print("timer measured", time_elapsed)
        assert run_time == time_elapsed
    else:
        print('Test done')

    # start-pause-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start_timer()

        # let timer run for some time
        run_time = random.randrange(0, 10)
        print("sleeping for", run_time, "seconds", end=" | ")
        time.sleep(run_time)

        timer.pause_timer()

        # pause the timer
        paused_time = random.randrange(0, 10)
        print("sleeping for", paused_time, "seconds", end=" | ")
        time.sleep(paused_time)

        # simulates the user not clicking the resume button
        # timer.resume_timer()

        timer.stop_timer()
        time_elapsed = timer.get_total_time_elapsed()
        print("timer measured", time_elapsed)
        assert run_time == time_elapsed
    else:
        print('Test done')
