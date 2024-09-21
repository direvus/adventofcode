"""Advent of Code 2017

Day 11: Hex Ed

https://adventofcode.com/2017/day/11
"""
import logging  # noqa: F401
from collections import namedtuple

from util import timing


# This hex grid uses a 2D coordinate system where the first axis is in the SE
# direction, and the second axis is in the SW direction.
Point = namedtuple('point', ['se', 'sw'])
Vector = namedtuple('vector', ['se', 'sw'])

DIRECTIONS = {
        'ne': Vector(-1, 0),
        'se': Vector(0, 1),
        's':  Vector(1, 1),
        'sw': Vector(1, 0),
        'nw': Vector(0, -1),
        'n':  Vector(-1, -1),
        }


def parse(stream) -> tuple:
    return stream.readline().strip().split(',')


def move(position: Point, direction: str) -> Point:
    v = DIRECTIONS[direction]
    return Point(position.se + v.se, position.sw + v.sw)


def get_distance(a: Point, b: Point) -> int:
    return max(abs(b.se - a.se), abs(b.sw - a.sw))


def follow_path(start: Point, directions: tuple) -> Point:
    position = start
    for d in directions:
        position = move(position, d)
    return position


def get_path_distance(directions: tuple) -> int:
    start = Point(0, 0)
    end = follow_path(start, directions)
    return get_distance(start, end)


def get_path_max_distance(directions: tuple) -> int:
    start = Point(0, 0)
    position = start
    result = float('-inf')
    for d in directions:
        position = move(position, d)
        result = max(result, get_distance(start, position))
    return result


def run(stream, test: bool = False):
    dirs = parse(stream)

    with timing("Part 1"):
        result1 = get_path_distance(dirs)

    with timing("Part 2"):
        result2 = get_path_max_distance(dirs)

    return (result1, result2)
