"""
Author: Samuel Dubovec
"""
import numpy as np
from numba import cuda
import math
import random


@cuda.jit
def compute_sum(numbers, results):
    """function which computes sums of lists from numbers list

    :param numbers: list of list for which we compute sums
    :param results: result list containing sums
    :return: None
    """
    index = cuda.grid(1)
    items = numbers[index]
    results[index] = sum(items)


def main():
    """ function which generates 256 lists of numbers from
    1 to random(8000, 10 000) computes sums for list in
    cuda environment

    :return: None
    """
    sums_to_compute = [
        list(np.arange(1, random.randint(8000, 10000))) for _ in range(256)
    ]
    results = np.ones(256)

    threads_per_block = 8
    blocks_per_grid = math.ceil(len(sums_to_compute) / threads_per_block)
    compute_sum[blocks_per_grid, threads_per_block](sums_to_compute, results)
    print(f'sums computed: {results}')


if __name__ == '__main__':
    main()
