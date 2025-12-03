"""Advent of Code 2025

Day 3: Lobby

https://adventofcode.com/2025/day/3
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return [line.strip() for line in stream if line.strip()]


def get_max_joltage(line: str):
    a = max(line[:-1])
    b = '0'
    for i, c in enumerate(line[:-1]):
        if c != a:
            continue
        n = max(line[i + 1:])
        if n > b:
            b = n
        if b == '9':
            break
    return int(a + b)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum([get_max_joltage(x) for x in parsed])

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
