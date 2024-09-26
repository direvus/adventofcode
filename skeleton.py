"""Advent of Code _YEAR_

Day _DAY_: _TITLE_

https://adventofcode.com/_YEAR_/day/_DAY_
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = 0

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
