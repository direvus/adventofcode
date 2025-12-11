"""Advent of Code 2025

Day 11: _TITLE_

https://adventofcode.com/2025/day/11
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
