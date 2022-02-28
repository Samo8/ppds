from fei.ppds import Thread, Mutex, Event, print


class SimpleBarrier:
    """class representing barrier, which has number of threads,
    counter, mutex and event as params.

    """
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()
        self.T.clear()


def before_barrier(thread_id):
    """Prints id of thread before barrier

    :param thread_id: id of thread calling the function
    :return: None
    """
    print(f"before barrier {thread_id}")


def after_barrier(thread_id):
    """Prints id of thread after barrier

    :param thread_id: id of thread calling the function
    :return: None
    """
    print(f"after barrier {thread_id}")


def barrier_cycle(b1, b2, thread_id):
    """Runs barrier infinite times

    :param b1: first barrier
    :param b2: second barrier
    :param thread_id: id of thread
    :return: None
    """
    while True:
        before_barrier(thread_id)
        b1.wait()
        after_barrier(thread_id)
        b2.wait()


def main():
    """Create two barriers and {threads_count} threads

    :return: None
    """
    threads_count = 5
    barrier1 = SimpleBarrier(threads_count)
    barrier2 = SimpleBarrier(threads_count)

    threads = [Thread(barrier_cycle, barrier1, barrier2, i) for i in range(threads_count)]
    [t.join() for t in threads]


main()
