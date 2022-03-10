"""
Author: Samuel Dubovec

@Copyright Matus Jokay
Implementation taken from pseudo code
"""
from fei.ppds import Mutex, Thread, Semaphore, Event, print
from time import sleep
from random import randint


class LS(object):
    """class representing Lightswitch object
    we have counter and simple mutex here"""

    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """function used to lock.
        :param sem: Semaphore which wait() is called on
        :return: None
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
    """class representing Lightswitch object
       we have counter and simple mutex here
       """

    def __init__(self):
        self.access_data = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = LS()
        self.ls_sensor = LS()
        self.valid_data = Event()


def monitor(shared, monitor_id):
    """function which simulates reading from
    2 monitors with delay of 500 ms

    :param shared: shared object
    :param monitor_id: id of current monitor
    :return: None
    """
    shared.valid_data.wait()
    while True:
        sleep(0.5)

        shared.turniket.wait()
        number_of_reading_monitors = shared.ls_monitor.lock(shared.access_data)
        shared.turniket.signal()

        print(f'monit{monitor_id}: '
              f'number_of_reading_monitors: {number_of_reading_monitors}\n')
        shared.ls_monitor.unlock(shared.access_data)


def sensor(shared, sensor_id):
    """function which represents writing by 10 sensors
    each write takes 10-15ms

    :param shared: shared object
    :param sensor_id: if of current sensor
    :return: None
    """
    while True:
        shared.turniket.wait()
        shared.turniket.signal()

        number_of_writing_sensors = shared.ls_sensor.lock(shared.access_data)

        write_duration = randint(10, 15) / 1000
        print(
            f'sensor {sensor_id}: '
            f'number_of_writing_sensors: {number_of_writing_sensors} '
            f'write_duration: {write_duration}\n')
        sleep(write_duration)

        shared.valid_data.signal()
        shared.ls_sensor.unlock(shared.access_data)


def main():
    """main function which creates 2 threads for monitors
    and 10 threads for sensors

    :return: None
    """
    shared = Shared()
    monitors = [Thread(monitor, shared, m) for m in range(2)]
    sensors = [Thread(sensor, shared, s) for s in range(10)]
    for thread in monitors + sensors:
        thread.join()


if __name__ == '__main__':
    main()
