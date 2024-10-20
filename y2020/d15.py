"""Advent of Code 2020

Day 15: Rambunctious Recitation

https://adventofcode.com/2020/day/15
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> tuple[int]:
    line = stream.readline().strip()
    return tuple(int(x) for x in line.split(','))


def get_nth_number(numbers: tuple[int], position: int) -> int:
    history = {}
    for i in range(len(numbers) - 1):
        history[numbers[i]] = i
    i += 1
    n = numbers[i]
    i += 1

    while i < position:
        if n in history:
            new = i - history[n] - 1
        else:
            new = 0
        history[n] = i - 1
        n = new
        i += 1
    return n


def run(stream, test: bool = False):
    with timing("Part 1"):
        numbers = parse(stream)
        result1 = get_nth_number(numbers, 2020)

    with timing("Part 2"):
        if test:
            # Part 2 is just more iterations of the same thing.
            result2 = 0
        else:
            result2 = get_nth_number(numbers, 30000000)

    return (result1, result2)
