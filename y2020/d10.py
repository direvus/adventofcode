"""Advent of Code 2020

Day 10: Adapter Array

https://adventofcode.com/2020/day/10
"""
import logging  # noqa: F401
from collections import Counter

from util import timing


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        line = line.strip()
        value = int(line)
        result.append(value)
    return result


def find_differences(adapters: list[int]) -> dict:
    diffs = []
    adapters.sort()
    value = 0
    for adapter in adapters:
        diff = adapter - value
        diffs.append(diff)
        value = adapter
    diffs.append(3)
    return Counter(diffs)


def run(stream, test: bool = False):
    with timing("Part 1"):
        adapters = parse(stream)
        diffs = find_differences(adapters)
        result1 = diffs[1] * diffs[3]

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
