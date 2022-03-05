"""
    Author: Samuel Dubovec

    This file contains example program for producer-consumer implementation
    using Lightswitch.

    ©Copyright
    This implementation is inspired by implementation at:
    https://www.youtube.com/watch?v=vI_DA3WiijI&t
    plot_graph function is taken from the same source.
"""
from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep
import matplotlib.pyplot as plt


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


class Shared(object):
    """Class representing P-C implementation
    we have count of produced and consumed items here
    """

    def __init__(self, N):
        self.ls = LS()
        self.finished = False
        self.semaphore = Semaphore(1)
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.produced_items_count = 0
        self.consumed_items_count = 0


def producer(shared, sleep_time):
    """producer function simulate production
    of items. Every produced item increase
    produced_items_count.
    Every produced item is printed to console.

    :param shared: shared instance
    :param sleep_time: time used for simulation production
    :return: None
    """
    while True:
        sleep(sleep_time)
        shared.produced_items_count += 1
        print(f'P: {shared.produced_items_count}')
        shared.free.wait()
        if shared.finished:
            break
        shared.ls.lock(shared.semaphore)
        sleep(randint(1, 10) / 100)
        shared.ls.unlock(shared.semaphore)
        shared.items.signal()


def consumer(shared, sleep_time):
    """consumer function simulate consumption
    of items. Every consumed item increase
    consumed_items_count.
    Every consumed item is printed to console.

    :param shared: shared instance
    :param sleep_time: time used for simulation consumption
    :return: None
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.ls.lock(shared.semaphore)
        sleep(randint(1, 10) / 100)
        shared.ls.unlock(shared.semaphore)
        shared.free.signal()
        shared.consumed_items_count += 1
        print(f'C: {shared.produced_items_count}')
        sleep(sleep_time)


def plot_graph(res):
    """function used for plotting graph with results.
    In graph, we have 3 values: consumption/production time,
    consumers number and consumers per second.

    :param res: list representing [x,y,z] values for graph
    :return: None
    """
    axes = plt.axes(projection='3d')
    axes.set_xlabel(
        'Consumption/production time (lower = more produced/consumed items)'
    )
    axes.set_ylabel('Consumers number')
    axes.set_zlabel('Consumed per second')
    x = [items[0] for items in res]
    y = [items[1] for items in res]
    z = [items[2] for items in res]
    axes.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    plt.show()


def main():
    result = []
    for i in range(1, 10):
        for consumers_number in range(1, 10):
            shared = Shared(10)

            sleep_time = i / 25
            p = [Thread(producer, shared, sleep_time) for _ in range(10)]
            c = [Thread(consumer, shared, sleep_time)
                 for _ in range(consumers_number)]

            sleep(4)
            shared.finished = True
            print(f'Hlavne vlakno:{i} caka')
            shared.items.signal(100)
            shared.free.signal(100)
            [t.join() for t in c + p]

            n_consumed_items = shared.consumed_items_count
            consumed_items_per_second = n_consumed_items / sleep_time

            result.append((sleep_time,
                           consumers_number,
                           consumed_items_per_second))

            print(f'Hlavne vlakno:{i} koniec')

    plot_graph(result)


if __name__ == '__main__':
    main()
