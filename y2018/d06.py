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


def get_orientation(a: tuple, b: tuple, c: tuple) -> float:
    """Return the orientation of a three point sequence.

    Return 0 if the points lie along the same line, a positive value if the
    orientation is clockwise and a negative value if it is counter-clockwise.
    """
    return (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])


def get_convex_hull(points: tuple) -> tuple:
    """Return the convex hull of this collection of points.

    Return the hull as a sequence of points.
    """
    points = sorted(points)
    result = []
    for p in points:
        result.append(p)
        while len(result) >= 3 and get_orientation(*result[-3:]) < 0:
            result.pop(-2)
    for p in tuple(reversed(points))[1:]:
        result.append(p)
        while len(result) >= 3 and get_orientation(*result[-3:]) < 0:
            result.pop(-2)
    return tuple(result)


def get_distances(point: tuple, points: tuple) -> list:
    return [(get_manhattan_distance(point, (x, y)), x, y) for x, y in points]


def find_finite_regions(points: tuple) -> dict:
    miny = INF
    minx = INF
    maxy = NINF
    maxx = NINF

    hull = get_convex_hull(points)
    logging.debug(hull)
    xs = tuple(p[0] for p in hull)
    ys = tuple(p[1] for p in hull)
    minx = min(xs) - 1
    maxx = max(xs) + 1
    miny = min(ys) - 1
    maxy = max(ys) + 1

    infinites = set(hull)
    regions = defaultdict(set)
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            p = (x, y)
            dists = get_distances(p, points)
            dists.sort()
            mind = dists[0][0]

            # Is it a clear winner or a tie?
            winners = [(x, y) for d, x, y in dists if d == mind]
            if len(winners) != 1:
                continue

            winner = winners[0]
            # Ignore regions that are infinite
            if winner in infinites:
                continue

            # If this point lies on the edge of the grid, mark this region as
            # infinite and don't record it
            if x in {minx, maxx} or y in {miny, maxy}:
                infinites.add(winner)
                # Remove this region if we've already recorded points for it
                regions.pop(winner, None)
                continue

            regions[winner].add((x, y))
    return regions


def find_largest_region(points: tuple) -> int:
    regions = find_finite_regions(points)
    return max(len(x) for x in regions.values())


def run(stream, test: bool = False):
    with timing("Part 1"):
        points = parse(stream)
        result1 = find_largest_region(points)

    with timing("Part 2"):
        limit = 32 if test else 10_000
        result2 = 0

    return (result1, result2)
