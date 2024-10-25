"""Advent of Code 2021

Day 1: _TITLE_

https://adventofcode.com/2021/day/1
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    result = []
    for line in stream:
        line = line.strip()
        result.append(int(line))
    return result


def count_increases(values) -> int:
    result = 0
    prev = values[0]
    for i in range(1, len(values)):
        if values[i] > prev:
            result += 1
        prev = values[i]
    return result


def count_window_increases(values, size) -> int:
    result = 0
    for i in range(size, len(values)):
        if values[i] > values[i - size]:
            result += 1
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = count_increases(parsed)

    with timing("Part 2"):
        result2 = count_window_increases(parsed, 3)

    return (result1, result2)
