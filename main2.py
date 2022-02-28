from fei.ppds import Thread, Semaphore, Event
from random import randint
from time import sleep


class Adt():
    """class which helds fibonacii sequence in list and list of semaphores/events
    needed for parallel computation

    """
    def __init__(self, N):
        self.N = N
        self.list = [0, 1] + [0] * N
        # initializing list of N + 1 semaphores, to avoid overflow when
        # signaling i+1 at the last index
        self.T = [Semaphore(0) for _ in range(N+1)]
        # initializing list of N + 1 events, to avoid overflow when
        # signaling i+1 at the last index
        # self.T =  [Event() for _ in range(N+1)]
        self.T[0].signal()


def compute_fibonacci(adt, i):
    """ function for computing fibonacci sequence

    :param adt: instance of Adt which has array of fibonacci in it with
                array of semaphores/events
    :param i: current thread index
    :return: None
    """
    sleep(randint(0, 10)/10)

    adt.T[i].wait()
    adt.list[i+2] = adt.list[i] + adt.list[i+1]
    adt.T[i+1].signal()


def main():
    """create {THREADS} threads and call compute_fibonacci for {THREADS} times.
    Prints computed fibonacci sequence to console.

    :return: None
    """
    THREADS = 10
    adt = Adt(THREADS)
    threads = [Thread(compute_fibonacci, adt, i) for i in range(THREADS)]
    [t.join() for t in threads]

    print(adt.list)


main()
