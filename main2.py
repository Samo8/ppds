"""
Author: Samuel Dubovec

This file contains example program for nuclear power plant 2
implementation
"""
from fei.ppds import Mutex, Thread, Semaphore, Event, print
from time import sleep
from random import randint


class LS(object):
    """class representing Lightswitch object
    we have counter and simple mutex here
    """

    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """function used to lock.
        :param sem: Semaphore which wait() is called on
        :return: counter value
        """
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
            self.mutex.unlock()
        return self.cnt

    def unlock(self, sem):
        """function used to unlock.
        :param sem: Semaphore which signal() is called on
        :return: None
        """
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()


class Shared:
    """class representing nuclear powerplant 2
    solution
    """

    def __init__(self):
        self.access_data = Semaphore(1)
        self.turniket = Semaphore(1)
        self.ls_monitor = LS()
        self.ls_sensor = LS()
        self.valid_data = Event()


def monitor(shared, monitor_id):
    """function which simulates reading data
    of 8 monitors, updating every 40- 50 ms

    :param shared: shared object
    :param monitor_id: id of current monitor
    :return: None
    """
    shared.valid_data.wait()
    while True:
        read_duration = randint(40, 50) / 1000
        sleep(read_duration)

        shared.turniket.wait()
        number_of_reading_monitors = shared.ls_monitor.lock(shared.access_data)
        shared.turniket.signal()
        print(
            f'monitor{monitor_id}: '
            f'number_of_reading_monitors: {number_of_reading_monitors} '
            f' read_duration: {read_duration}\n')
        shared.ls_monitor.unlock(shared.access_data)


def sensor(shared, sensor_id):
    """function which simulates writing data
    by 3 sensors. 2 sensors write in duration 10-20 ms
    and the third sensor in 20-25ms.

    :param shared: shared object
    :param sensor_id: od of current sensor
    :return: None
    """
    while True:
        sleep_time = randint(50, 60) / 1000
        sleep(sleep_time)

        shared.turniket.wait()
        number_of_writing_sensors = shared.ls_sensor.lock(shared.access_data)
        shared.turniket.signal()

        if sensor_id == 2:
            write_duration = randint(20, 25) / 1000
        else:
            write_duration = randint(10, 20) / 1000

        print(f'sensor {sensor_id}:  '
              f'number_of_writing_sensors: {number_of_writing_sensors}, '
              f'write_duration: {write_duration}\n')
        sleep(write_duration)
        shared.valid_data.signal()
        shared.ls_sensor.unlock(shared.access_data)


def main():
    """main function which creates 8 threads for monitors
    and 3 thread for sensors

    :return: None
    """
    shared = Shared()
    monitors = [Thread(monitor, shared, m) for m in range(8)]
    sensors = [Thread(sensor, shared, s) for s in range(3)]
    for thread in monitors + sensors:
        thread.join()


if __name__ == '__main__':
    main()
