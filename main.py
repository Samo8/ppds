"""
Author: Samuel Dubovec
"""
import sys


class Scheduler(object):
    """class representing Scheduler which holds list/queue
    of coprograms - foo and bar
    """
    def __init__(self, coprograms):
        self.coprograms = coprograms

    def run(self):
        """function run represents running of coprograms
        we store coprograms in list/queue and get/add them from/to it

        :return: None
        """
        while True:
            task = self.coprograms.pop(0)
            task.send(None)
            self.coprograms.append(task)


def main(iteration_number=sys.maxsize):
    """main function creates two functions (coprograms) foo and bar

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
