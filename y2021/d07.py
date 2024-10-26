"""Advent of Code 2021

Day 7: Treachery of Whales

https://adventofcode.com/2021/day/7
"""
import logging  # noqa: F401
from functools import cache

from util import timing, INF


def parse(stream) -> tuple[int]:
    line = stream.readline().strip()
    return tuple(int(x) for x in line.split(','))


def find_alignment(positions: tuple[int]) -> int:
    best = INF
    first, last = min(positions), max(positions)
    for i in range(first, last + 1):
        cost = sum(abs(p - i) for p in positions)
        logging.debug(f'cost to reach {i} is {cost}')
        if cost < best:
            best = cost
    return best


@cache
def get_cost(distance: int) -> int:
    return distance * (distance + 1) // 2


def find_alignment2(positions: tuple[int]) -> int:
    best = INF
    first, last = min(positions), max(positions)
    for i in range(first, last + 1):
        cost = sum(get_cost(abs(i - p)) for p in positions)
        logging.debug(f'cost to reach {i} is {cost}')
        if cost < best:
            best = cost
    return best


def run(stream, test: bool = False):
    with timing("Part 1"):
        positions = parse(stream)
        result1 = find_alignment(positions)

    with timing("Part 2"):
        result2 = find_alignment2(positions)

    return (result1, result2)
