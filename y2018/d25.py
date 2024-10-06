"""Advent of Code 2018

Day 25: Four-Dimensional Adventure

https://adventofcode.com/2018/day/25
"""
import logging  # noqa: F401
from collections import namedtuple  # noqa: F401

from util import get_manhattan_distance, timing


P = namedtuple('P', ('x', 'y', 'z', 't'))


def parse(stream) -> list[P]:
    if isinstance(stream, str):
        stream = stream.split('\n')

    result = []
    for line in stream:
        line = line.strip()
        if not line:
            continue
        point = P(*(int(x) for x in line.split(',')))
        result.append(point)
    return result


def is_within(point: P, group: set[P], distance: int = 3) -> bool:
    """Return whether a point is close to a group of points.

    Return True if any of the points in `group` is within `distance` of the
    `point`, and False otherwise.
    """
    for p in group:
        if get_manhattan_distance(point, p) <= distance:
            return True
    return False


def constellate(points: list[P]) -> list:
    groups = {}
    i = 0
    for p in points:
        matched = None
        merged = set()
        for k, g in groups.items():
            if is_within(p, g, 3):
                if matched is None:
                    g.add(p)
                    matched = k
                else:
                    # merge this group into the first matched
                    groups[matched] |= g
                    g.clear()
                    merged.add(k)
        if matched is None:
            # No existing group matches, start a new one.
            groups[i] = {p}
            i += 1
        # delete any groups that got merged into others
        for key in merged:
            del groups[key]
    return groups


def count_constellations(points: list[P]) -> int:
    groups = constellate(points)
    return len(groups)


def run(stream, test: bool = False):
    with timing("Part 1"):
        points = parse(stream)
        result1 = count_constellations(points)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
