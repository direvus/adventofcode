"""Advent of Code 2024

Day 2: Red-Nosed Reports

https://adventofcode.com/2024/day/2
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list:
    result = []
    for line in stream:
        words = line.strip().split()
        result.append(tuple(int(x) for x in words))
    return result


def is_safe(values) -> bool:
    increasing = None
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        if increasing is None:
            increasing = diff > 0
        elif (diff > 0) != increasing:
            return False

        if abs(diff) < 1 or abs(diff) > 3:
            return False
    return True


def is_safe_dampener(values) -> bool:
    if is_safe(values):
        return True

    for i in range(len(values)):
        report = values[:i] + values[i + 1:]
        if is_safe(report):
            return True
    return False


def run(stream, test: bool = False):
    with timing("Part 1"):
        reports = parse(stream)
        result1 = sum(int(is_safe(x)) for x in reports)

    with timing("Part 2"):
        result2 = sum(int(is_safe_dampener(x)) for x in reports)

    return (result1, result2)
