import asyncio
import time


async def compute_sum(numbers):
    total = 0
    for number in numbers:
        await asyncio.sleep(0.2)
        total += number
    return total


async def sum_numbers(name, numbers):
    print(f'Computing sum {name} for numbers: {numbers}')
    total = await compute_sum(numbers)
    print(f'Task {name}, Sum = {total}\n')


async def main():
    tasks = [
        sum_numbers("small", [1, 2]),
        sum_numbers("big", [1, 2, 3, 4, 5, 6, 7, 8]),
        sum_numbers("medium", [1, 2, 3, 4, 5]),
        sum_numbers("huge", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
    ]
    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == '__main__':
    asyncio.run(main())
