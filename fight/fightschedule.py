import threading
import time


class FightSchedule:

    __rooms = []

    def __init__(self):
        self.thread = ScheduleThread("ScheduleThread", self)
        self.thread.start()

    def run_frame(self, loop_time):
        for room in self.__rooms:
            if room.check_end():
                self.unschedule(room)
            room.update(loop_time)

    def schedule(self, room):
        self.__rooms.append(room)

    def unschedule(self, room):
        self.__rooms.remove(room)


class ScheduleThread(threading.Thread):

    __interval = 0.05

    def __init__(self, name, schedule):
        threading.Thread.__init__(self)
        self.__name = name
        self.schedule = schedule

    def run(self):
        current_time = time.time()
        while threading.currentThread().isAlive():
            loop_time = time.time() - current_time
            current_time = time.time()
            if loop_time < self.__interval:
                time.sleep(self.__interval - loop_time)
            else:
                self.schedule.run_frame(loop_time)

