"""Advent of Code 2019

Day 16: Flawed Frequency Transmission

https://adventofcode.com/2019/day/16
"""
import logging  # noqa: F401
from itertools import cycle

from util import timing


BASE = (0, 1, 0, -1)


def expand_pattern(pattern, repeats: int):
    for item in cycle(pattern):
        for _ in range(repeats):
            yield item


def get_element(inputs, pattern, index: int) -> int:
    result = 0
    iterator = expand_pattern(pattern, index + 1)
    # Discard the first element of the expanded pattern
    next(iterator)
    for item in inputs:
        pattern_value = int(next(iterator))
        result += item * pattern_value
    return abs(result) % 10


def do_phase(inputs, pattern) -> tuple:
    result = []
    for i in range(len(inputs)):
        result.append(get_element(inputs, pattern, i))
    return tuple(result)


def do_phases(inputs, pattern, count: int) -> tuple:
    signal = inputs
    for _ in range(count):
        signal = do_phase(signal, pattern)
    return signal


def parse(stream) -> tuple[int]:
    line = stream.readline().strip()
    return tuple(int(x) for x in line)


def run(stream, test: bool = False):
    with timing("Part 1"):
        signal = parse(stream)
        output = do_phases(signal, BASE, 100)
        result1 = ''.join(str(x) for x in output[:8])

    with timing("Part 2"):
        signal = signal * 10_000
        offset = int(''.join(str(x) for x in signal[:7]))
        result2 = 0

    return (result1, result2)
