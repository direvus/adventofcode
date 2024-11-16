"""Advent of Code 2022

Day 1: Calorie Counting

https://adventofcode.com/2022/day/1
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    result = []
    items = []
    for line in stream:
        line = line.strip()
        if line == '':
            result.append(items)
            items = []
            continue
        items.append(int(line))
    if items:
        result.append(items)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        totals = [sum(x) for x in parsed]
        result1 = max(totals)

    with timing("Part 2"):
        totals.sort(reverse=True)
        top = totals[:3]
        result2 = sum(top)

    return (result1, result2)
