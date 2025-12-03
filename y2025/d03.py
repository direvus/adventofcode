"""Advent of Code 2025

Day 3: Lobby

https://adventofcode.com/2025/day/3
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return [line.strip() for line in stream if line.strip()]


def get_max_joltage(line: str, count: int):
    if count == 1:
        return max(line)
    limit = -(count - 1)
    a = max(line[:limit])
    b = '0'
    for i, c in enumerate(line[:limit]):
        if c != a:
            continue
        n = get_max_joltage(line[i + 1:], count - 1)
        if n > b:
            b = n
    return a + b


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum([int(get_max_joltage(x, 2)) for x in parsed])

    with timing("Part 2"):
        result2 = sum([int(get_max_joltage(x, 12)) for x in parsed])

    return (result1, result2)
