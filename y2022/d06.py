"""Advent of Code 2022

Day 6: Tuning Trouble

https://adventofcode.com/2022/day/6
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return stream.readline().strip()


def find_marker(line: str, count: int = 4) -> int:
    for i in range(count, len(line)):
        if len(set(line[i - count: i])) == count:
            return i


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = find_marker(parsed)

    with timing("Part 2"):
        result2 = find_marker(parsed, 14)

    return (result1, result2)
