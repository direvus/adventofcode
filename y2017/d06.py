"""Advent of Code 2017

Day 6: Memory Reallocation

https://adventofcode.com/2017/day/6
"""
from util import timing


def parse(stream) -> tuple[int]:
    return tuple(int(word) for word in stream.readline().strip().split())


def count_cycles(banks: tuple[int]) -> tuple:
    """Count the number of cycles until we revist any state.

    Return a tuple containing the number of cycles, and the state that
    was revisited to trigger the end of the count.
    """
    counter = 0
    configs = set()
    banks = list(banks)
    length = len(banks)
    while tuple(banks) not in configs:
        configs.add(tuple(banks))
        largest = float('-inf')
        winner = None
        for i, blocks in enumerate(banks):
            if blocks > largest:
                largest = blocks
                winner = i
        banks[winner] = 0
        i = (winner + 1) % length
        while largest > 0:
            banks[i] += 1
            largest -= 1
            i = (i + 1) % length
        counter += 1
    return counter, tuple(banks)


def count_cycles_to(banks: tuple[int], target: tuple) -> int:
    """Count the number of cycles until we revist a specific state."""
    counter = 0
    banks = list(banks)
    length = len(banks)
    while counter == 0 or tuple(banks) != target:
        largest = float('-inf')
        winner = None
        for i, blocks in enumerate(banks):
            if blocks > largest:
                largest = blocks
                winner = i
        banks[winner] = 0
        i = (winner + 1) % length
        while largest > 0:
            banks[i] += 1
            largest -= 1
            i = (i + 1) % length
        counter += 1
    return counter


def run(stream, test=False):
    banks = parse(stream)
    with timing("Part 1"):
        result1, config = count_cycles(banks)
    with timing("Part 2"):
        result2 = count_cycles_to(config, config)

    return (result1, result2)
