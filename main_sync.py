"""
Author: Samuel Dubovec
"""
import time


def compute_sum(numbers):
    """function for computing sum of numbers given as param

    :param numbers: list of numbers to compute sum of
    :return: None
    """
    total = 0
    for number in numbers:
        time.sleep(0.2)
        total += number
    return total


def sum_numbers(name, numbers):
    """function printing info about sum which is being computed
    computation is done in sync way

    :param name: name corresponds to numbers list
    :param numbers: list of numbers to compute sum of
    :return: None
    """
    print(f'Computing sum {name} for numbers: {numbers}')
    total = compute_sum(numbers)
    print(f'Task {name}, Sum = {total}\n')
    yield


def main():
    """function creates tasks array which contains
    coprograms sum_numbers with various list lengths to compute sum

    :return: None
    """
    tasks = [
        sum_numbers("small", [1, 2]),
        sum_numbers("big", [1, 2, 3, 4, 5, 6, 7, 8]),
        sum_numbers("medium", [1, 2, 3, 4, 5]),
        sum_numbers("huge", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
    ]

    done = False
    time_start = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)

            if not tasks:
                done = True
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == "__main__":
    main()
