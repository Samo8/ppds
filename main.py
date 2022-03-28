"""
Author: Samuel Dubovec

@Copyright Matus Jokay
Implementation inspired by pseudocode from lecture
"""
from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep

N = 5
MAX_CUSTOMER = 7


class Shared:
    """class representing customers and barber
    we have semaphore for customer, semaphores for
    signalizing that customer and barber is done and
    queue of barbers, one for each customer
    """

    def __init__(self):
        self.customers = 0
        self.customer = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.mutex = Mutex()
        self.queue = []


def barber(shared):
    """function representing barber, barber cuts customer's hair
    each customer has own barber, which we take from queue

    :param shared: shared object holding necessary data
    :return: None
    """
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        barber_of_customer = shared.queue.pop(0)
        shared.mutex.unlock()
        barber_of_customer.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


def customer(shared, i):
    """function representing customer
    we could have max N number of customer in barbershop
    customer is getting haircut by barber

    :param shared: sahred object holding necessary data
    :param i: customer id
    :return: None
    """
    while True:
        grow_hair(i)

        shared.mutex.lock()
        if shared.customers == N:
            balk(i)
            shared.mutex.unlock()
            continue

        shared.customers += 1
        barber_of_customer = Semaphore(0)
        shared.queue.append(barber_of_customer)
        shared.mutex.unlock()

        shared.customer.signal()
        barber_of_customer.wait()

        get_hair_cut(i)
        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.customers -= 1
        print(f'Customer {i} is done, there are '
              f'{shared.customers} customers waiting for the haircut')
        shared.mutex.unlock()


def grow_hair(i):
    """function representing growing of hair
    function give additional time for barber to cut hair,
    so there are not always customers trying to get into barbershop

    :param i: customer id
    :return: None
    """
    print(f'Customer: {i} waiting for hair to grow')
    sleep(randint(250, 450) / 1000)


def cut_hair():
    """function representing cutting of hair by barber

    :return: None
    """
    sleep(randint(50, 150) / 100)
    print(f'Barber: cutting hair of customer')


def balk(i):
    """function representing leaving of customer
    in case barbershop is full

    :param i: customer id
    :return: None
    """
    print(f'Barbershop is full --> customer {i} is leaving')


def get_hair_cut(i):
    """function representing getting haircut by barber of customer

    :param i: customer id
    :return: None
    """
    sleep(randint(50, 150) / 100)
    print(f'Customer {i} is getting haircut')


def main():
    """main function which creates MAX_CUSTOMERS threads for customer
    and one thread for barber

    :return: None
    """
    shared = Shared()
    customers = [Thread(customer, shared, i) for i in range(MAX_CUSTOMER)]
    barber_t = Thread(barber, shared)

    for t in customers:
        t.join()
    barber_t.join()


if __name__ == '__main__':
    main()
