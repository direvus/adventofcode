"""Advent of Code 2020

Day 1: Report Repair

https://adventofcode.com/2020/day/1
"""
import logging  # noqa: F401

from util import timing
from itertools import combinations


def parse(stream) -> tuple[int]:
    return tuple(int(x.strip()) for x in stream)


def find_sum_entries(values: tuple, target: int, size: int) -> tuple | None:
    for comb in combinations(values, size):
        if sum(comb) == target:
            return comb


def run(stream, test: bool = False):
    with timing("Part 1"):
        values = parse(stream)
        a, b = find_sum_entries(values, 2020, 2)
        result1 = a * b

    with timing("Part 2"):
        a, b, c = find_sum_entries(values, 2020, 3)
        result2 = a * b * c

    return (result1, result2)
