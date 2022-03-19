"""
Author: Samuel Dubovec

This file contains example program for savages 2 task
"""
from random import randint
from time import sleep
from fei.ppds import Thread, print, Semaphore, Mutex, Event

N = 6
M = 4
cooks_number = 4


class SimpleBarrier(object):
    """class representing barrier
    """
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, shared):
        """method used to wait while using SimpleBarrier
        the last cook which calls this method signals
        that pot is full and increases servings

        :param shared: object representing shared param
        :return: None
        """
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.barrier.signal(self.N)
            shared.full_pot.signal()
            shared.servings += M
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    """class representing savages 2 solution
    """
    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Event()
        self.full_pot = Semaphore(0)
        self.b1_cook = SimpleBarrier(cooks_number)


def eat(i):
    """function representing eating by savage

    :param i: savage id
    :return: None
    """
    print(f'savage {i} eat start')
    sleep(randint(50, 200) / 100)
    print(f'savage {i} eat end')


def savage(i, shared):
    """function representing savage
    savages can eat while there is
    something in pot

    :param i: savage id
    :param shared: shared object
    :return: None
    """
    sleep(randint(1, 100) / 100)
    while True:
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: empty pot')
            shared.empty_pot.signal()
            shared.empty_pot.clear()
            shared.full_pot.wait()
        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(i, shared):
    """function representing cook
    last cook signalize that pot is full

    :param i: cook id
    :param shared: shared object
    :return: None
    """
    while True:
        shared.empty_pot.wait()

        print(f'cook: {i} cooking')
        sleep(50 / 1000)
        print(f'cook: {i} servings --> pot')

        shared.b1_cook.wait(shared)


def main():
    """main function which creates N savages threads
    and cook_number cooks threads

    :return: None
    """
    shared = Shared(0)
    savages = []
    cooks = []

    for i in range(N):
        savages.append(Thread(savage, i, shared))
    for i in range(cooks_number):
        cooks.append(Thread(cook, i, shared))

    for t in savages + cooks:
        t.join()


if __name__ == '__main__':
    main()
