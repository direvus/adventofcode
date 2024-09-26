"""Advent of Code 2018

Day 6: Chronal Coordinates

https://adventofcode.com/2018/day/6
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing, INF, NINF, get_manhattan_distance


def parse(stream) -> tuple:
    result = []
    for line in stream:
        line = line.strip()
        result.append(tuple(int(x) for x in line.split(', ')))
    return tuple(result)


def get_distances(point: tuple, points: tuple) -> list:
    return [(get_manhattan_distance(point, (x, y)), x, y) for x, y in points]


def find_largest_region(points: tuple) -> int:
    miny = INF
    minx = INF
    maxy = NINF
    maxx = NINF

    counter = {}
    for x, y in points:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
        counter[(x, y)] = 0

    regions = defaultdict(lambda: 0)
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            p = (x, y)
            dists = get_distances(p, points)
            dists.sort()
            mind = dists[0][0]

            # Is it a clear winner or a tie?
            winners = [(x, y) for d, x, y in dists if d == mind]
            if len(winners) == 1:
                regions[winners[0]] += 1
    logging.debug(regions)


def run(stream, test: bool = False):
    with timing("Part 1"):
        points = parse(stream)
        result1 = find_largest_region(points)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
