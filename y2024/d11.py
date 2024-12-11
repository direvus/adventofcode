"""Advent of Code 2024

Day 11: Plutonian Pebble

https://adventofcode.com/2024/day/11
"""
import logging  # noqa: F401
from functools import cache

from util import timing


def parse(stream) -> str:
    return tuple(map(int, stream.readline().strip().split()))


def expand_value(value: int) -> list:
    if value == 0:
        return [1]

    text = str(value)
    length = len(text)
    if length % 2 == 0:
        i = length // 2
        a = int(text[:i])
        b = int(text[i:])
        return [a, b]

    return [value * 2024]


@cache
def count_stones(value: int, count: int):
    if count == 0:
        return 1
    values = expand_value(value)
    return sum(count_stones(x, count - 1) for x in values)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(count_stones(x, 25) for x in parsed)

    with timing("Part 2"):
        result2 = sum(count_stones(x, 75) for x in parsed)

    return (result1, result2)
