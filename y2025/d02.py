"""Advent of Code 2025

Day 2: Gift Shop

https://adventofcode.com/2025/day/2
"""
import logging  # noqa: F401
import re

from util import timing


PATTERN = re.compile(r'^(\d+)\1+$')


def parse(stream) -> str:
    parts = stream.readline().strip().split(',')
    ranges = [x.split('-') for x in parts]
    return [(int(a), int(b)) for a, b in ranges]


def is_invalid(n: int) -> bool:
    text = str(n)
    length = len(text)
    if length % 2 != 0:
        # Odd number of digits, cannot be invalid
        return False

    i = length // 2
    return text[:i] == text[i:]


def is_invalid_2(n: int) -> bool:
    text = str(n)
    return PATTERN.fullmatch(text)


def sum_invalid(a: int, b: int):
    return sum([x if is_invalid(x) else 0 for x in range(a, b + 1)])


def sum_invalid_2(a: int, b: int):
    return sum([x if is_invalid_2(x) else 0 for x in range(a, b + 1)])


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum([sum_invalid(a, b) for a, b in parsed])

    with timing("Part 2"):
        result2 = sum([sum_invalid_2(a, b) for a, b in parsed])

    return (result1, result2)
