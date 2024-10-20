"""Advent of Code 2020

Day 13: Shuttle Search

https://adventofcode.com/2020/day/13
"""
import logging  # noqa: F401
from math import ceil

from util import timing


def parse(stream) -> tuple[int, list]:
    line = stream.readline().strip()
    time = int(line)
    line = stream.readline().strip()
    buses = [int(x) if x != 'x' else None for x in line.split(',')]
    return (time, buses)


def find_earliest_bus(start: int, buses: set[int]) -> tuple:
    stops = {x * ceil(start / x): x for x in buses}
    nextstop = min(stops.keys())
    nextbus = stops[nextstop]

    return (nextstop - start, nextbus)


def run(stream, test: bool = False):
    with timing("Part 1"):
        start, routes = parse(stream)
        buses = {x for x in routes if x is not None}
        wait, bus = find_earliest_bus(start, buses)
        result1 = wait * bus

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
