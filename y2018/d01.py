"""Advent of Code 2018

Day 1: Chronal Calibration

https://adventofcode.com/2018/day/1
"""
import logging  # noqa: F401
from itertools import cycle

from util import timing


def parse(stream) -> tuple:
    result = []
    for line in stream:
        line = line.strip()
        words = line.split(', ')
        result.extend((int(x) for x in words))
    return result


def find_first_repeat(sequence: tuple) -> int:
    values = set()
    current = 0
    for change in cycle(sequence):
        current += change
        if current in values:
            return current
        values.add(current)


def run(stream, test: bool = False):
    with timing("Part 1"):
        sequence = parse(stream)
        result1 = sum(sequence)

    with timing("Part 2"):
        result2 = find_first_repeat(sequence)

    return (result1, result2)
