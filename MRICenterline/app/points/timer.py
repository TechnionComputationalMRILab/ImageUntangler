from typing import List
from datetime import datetime, timezone, timedelta
from MRICenterline.app.points.status import TimerStatus

import logging
logging.getLogger(__name__)


class Timer:
    """ Basic stopwatch with pause/resume functionality """

    def __init__(self):
        self.status: TimerStatus = TimerStatus.STOPPED
        self.measured_gap: float = 0.0
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.resume_time = None
        self.time_gap: List[timedelta] = []

    def reset_timer(self):
        self.__init__()

    def command(self, command):
        if command == 'START':
            self.start()
        elif command == "STOP":
            self.stop()
        elif command == "PAUSE":
            self.pause()
        elif command == "RESUME":
            self.resume()
        else:
            raise KeyError("Timer function not defined")

    def start(self):
        self.status = TimerStatus.RUNNING
        self.start_time = datetime.now(timezone.utc).astimezone()
    
    def stop(self):
        if self.status == TimerStatus.PAUSED:
            # if the timer is paused, it will resume and then stop so that the time gap will be recorded
            self.resume()

        self.status = TimerStatus.STOPPED
        self.stop_time = datetime.now(timezone.utc).astimezone()
            
    def pause(self):
        self.status = TimerStatus.PAUSED
        self.pause_time = datetime.now(timezone.utc).astimezone()
    
    def resume(self):
        self.status = TimerStatus.RUNNING
        self.resume_time = datetime.now(timezone.utc).astimezone()
        
        self.time_gap.append(self.resume_time - self.pause_time)

    def calculate_time_gap(self):
        if self.start_time is None:
            # timer was never started
            return 0.0
        
        if self.status == TimerStatus.STOPPED:
            measured_time = self.stop_time - self.start_time - sum(self.time_gap, timedelta())

            return int(measured_time.total_seconds())
        else:
            self.stop()
            return self.calculate_time_gap()


if __name__ == "__main__":
    import time
    import random
    test_num = 5

    # basic start-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start()
        pause = random.randrange(0, 10)
        print("sleeping for", pause, "seconds", end=" | ")
        time.sleep(pause)
        timer.stop()
        time_elapsed = timer.calculate_time_gap()
        print("timer measured", time_elapsed)
        assert pause == round(time_elapsed)
    else:
        print('Basic test done')

    # start-(pause/resume)-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start()

        # let timer run for some time
        run_time = random.randrange(0, 10)
        print("running for", run_time, "seconds", end=" | ")
        time.sleep(run_time)

        timer.pause()

        # pause the timer
        paused_time = random.randrange(0, 10)
        print("pausing for", paused_time, "seconds", end=" | ")
        time.sleep(paused_time)

        timer.resume()

        timer.stop()
        time_elapsed = timer.calculate_time_gap()
        print("timer measured", time_elapsed)
        assert run_time == round(time_elapsed)
    else:
        print('Test done')

    # start-pause-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start()

        # let timer run for some time
        run_time = random.randrange(0, 10)
        print("running for", run_time, "seconds", end=" | ")
        time.sleep(run_time)

        timer.pause()

        # pause the timer
        paused_time = random.randrange(0, 10)
        print("pausing for", paused_time, "seconds", end=" | ")
        time.sleep(paused_time)

        # simulates the user not clicking the resume button
        # timer.resume()

        timer.stop()
        time_elapsed = timer.calculate_time_gap()
        print("timer measured", time_elapsed)
        assert run_time == round(time_elapsed)
    else:
        print('Test done')

    # start-rand*(pause/resume)-stop functionality
    for _ in range(test_num):
        timer = Timer()
        timer.start()

        # let timer run for some time
        run_time = random.randrange(0, 10)
        print("running for", run_time, "seconds", end=" | ")
        time.sleep(run_time)

        loop_count = random.randrange(0, 5)
        for _ in range(loop_count):
            timer.pause()

            # pause the timer
            paused_time = random.randrange(0, 10)
            print("pausing for", paused_time, "seconds", end=" | ")
            time.sleep(paused_time)

            timer.resume()

            # let timer run more
            extra_run_time = random.randrange(0, 10)
            print("running for", extra_run_time, "seconds", end=" | ")
            time.sleep(extra_run_time)
            run_time += extra_run_time

        timer.stop()
        time_elapsed = timer.calculate_time_gap()
        print("timer measured", time_elapsed)
        assert run_time == round(time_elapsed)
    else:
        print('Test done')
