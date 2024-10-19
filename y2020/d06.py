"""Advent of Code 2020

Day 6: Custom Customs

https://adventofcode.com/2020/day/6
"""
import logging  # noqa: F401
import operator
from functools import reduce

from util import timing


def parse(stream) -> list[list]:
    result = []
    group = []
    for line in stream:
        line = line.strip()
        if line == '':
            if group:
                result.append(group)
            group = []
            continue
        group.append({c for c in line})
    if group:
        result.append(group)
    return result


def get_sum_union(groups: list[list]) -> int:
    result = 0
    for group in groups:
        result += len(reduce(operator.or_, group))
    return result


def get_sum_intersection(groups: list[list]) -> int:
    result = 0
    for group in groups:
        result += len(reduce(operator.and_, group))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        groups = parse(stream)
        result1 = get_sum_union(groups)

    with timing("Part 2"):
        result2 = get_sum_intersection(groups)

    return (result1, result2)
