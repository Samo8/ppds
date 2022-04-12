"""
Author: Samuel Dubovec
"""
import sys


class Scheduler(object):
    """class representing Scheduler which holds list/queue
    of coroutines - foo and bar
    """
    def __init__(self, coroutines):
        self.coroutines = coroutines

    def run(self):
        """function run represents running of coroutines
        we store coroutines in list/queue and get/add them from/to it

        :return: None
        """
        while True:
            task = self.coroutines.pop(0)
            task.send(None)
            self.coroutines.append(task)


def main(iteration_number=sys.maxsize):
    """main function creates two functions (coroutines) foo and bar

    :param iteration_number: represents number of iterations
    if not set, runs infinity
    :return: None
    """
    def foo():
        """foo prints to console and yields value iteration_number times

        :return: None
        """
        for _ in range(iteration_number):
            print('I\'m foo')
            yield

    def bar():
        """bar prints to console and yields value iteration_number times

        :return: None
        """
        for _ in range(iteration_number):
            print('I\'m bar')
            yield

    scheduler = Scheduler([foo(), bar()])
    try:
        scheduler.run()
    except StopIteration:
        print('I have reached the end')


if __name__ == '__main__':
    main(6)
