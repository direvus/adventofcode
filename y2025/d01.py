"""Advent of Code 2025

Day 1: Secret Entrance

https://adventofcode.com/2025/day/1
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        n = int(line[1:])
        if line[0] == 'L':
            n = -n
        result.append(n)
    return result


def count_zeroes(steps):
    result = 0
    pos = 50
    for step in steps:
        pos = (pos + step) % 100
        if pos == 0:
            result += 1
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = count_zeroes(parsed)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
