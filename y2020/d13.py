"""Advent of Code 2020

Day 13: Shuttle Search

https://adventofcode.com/2020/day/13
"""
import logging  # noqa: F401
from math import ceil

from util import timing, NINF


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


def is_valid(time: int, routes: tuple[tuple[int, int]]) -> bool:
    return all((time + i) % bus == 0 for i, bus in routes)


def find_consecutive_time(routes: list[int | None]) -> int:
    """Find the earliest time where buses depart consecutively.

    This is the earliest timestamp such that the first bus listed in the
    timetable departs at that time, and second bus listed departs the following
    minute, and so on. Routes marked with 'x' in the input (None in the
    `routes` argument) are unconstrained but do occupy a time slot in the
    departure sequence.
    """
    largest = NINF
    index = 0
    r = []
    for i, x in enumerate(routes):
        if x is None:
            continue
        r.append((i, x))
        if x > largest:
            largest = x
            index = i
    time = largest - index

    while True:
        if is_valid(time, r):
            return time
        time += largest


def run(stream, test: bool = False):
    with timing("Part 1"):
        start, routes = parse(stream)
        buses = {x for x in routes if x is not None}
        wait, bus = find_earliest_bus(start, buses)
        result1 = wait * bus

    with timing("Part 2"):
        result2 = find_consecutive_time(routes)

    return (result1, result2)
