"""Advent of Code 2024

Day 3: _TITLE_

https://adventofcode.com/2024/day/3
"""
import logging  # noqa: F401
import re

from util import timing


PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')


def parse(stream) -> str:
    return stream.read()


def run(stream, test: bool = False):
    with timing("Part 1"):
        line = parse(stream)
        matches = PATTERN.findall(line)
        result1 = sum(int(a) * int(b) for a, b in matches)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
