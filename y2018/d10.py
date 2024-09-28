"""Advent of Code 2018

Day 10: The Stars Align

https://adventofcode.com/2018/day/10
"""
import logging  # noqa: F401
import math
import re
from collections import namedtuple
from itertools import combinations

from util import timing, get_manhattan_distance, INF


Ray = namedtuple('Light', ['px', 'py', 'vx', 'vy'])
PATTERN = re.compile(r'-?\d+')


def parse(stream) -> tuple:
    result = []
    for line in stream:
        line = line.strip()
        ray = Ray(*(int(x) for x in PATTERN.findall(line)))
        result.append(ray)
    return result


def find_intersection(a: Ray, b: Ray) -> tuple | None:
    """Return the intersection of two non-vertical rays.

    If an intersection will occur, return a 3-tuple containing the X and Y
    coordinates and the time of intersection.

    If no intersection will occur (the rays are parallel or would have
    intersected in the past), or if either of the rays are vertical, then
    return None.
    """
    assert a != b
    # Vertical cases might intersect, but for the purposes of this puzzle we
    # are not going to bother with them.
    if a.vx == 0 or b.vx == 0:
        return None

    grada = a.vy / a.vx
    gradb = b.vy / b.vx
    convergence = grada - gradb
    if convergence == 0:
        return None

    ydist = b.py + (a.px - b.px) * gradb - a.py
    x = a.px + ydist / convergence
    y = a.py + (x - a.px) * grada
    t = (x - a.px) / a.vx
    if t > 0:
        return x, y, t


def get_total_distance(points: tuple) -> int:
    result = 0
    for a, b in combinations(points, 2):
        result += get_manhattan_distance(a, b)
    return result


def find_message_time(rays: tuple) -> int:
    """Find the time when the message should appear.

    Work through pairs of rays and record all the pairs that have a simple
    intersection at some future time. Then work through those times and find
    the one that has the least total distance between points.
    """
    times = []
    for a, b in combinations(rays, 2):
        if a == b:
            continue
        s = find_intersection(a, b)
        if s is not None:
            x, y, t = s
            if t > 1:
                times.append(math.floor(t))

    best = INF
    time = None
    for t in range(min(times), max(times) + 1):
        points = advance(rays, t)
        dist = get_total_distance(points)
        if dist < best:
            best = dist
            time = t
    return time


def advance(rays: tuple, time: int) -> tuple:
    """Advance all rays by the given time value.

    Return a tuple of (X, Y) points.
    """
    result = []
    for ray in rays:
        new = (ray.px + ray.vx * time, ray.py + ray.vy * time)
        result.append(new)
    return tuple(result)


def points_to_string(points: tuple) -> str:
    xs = tuple(p[0] for p in points)
    ys = tuple(p[1] for p in points)
    minx = min(xs) - 1
    maxx = max(xs) + 1
    miny = min(ys) - 1
    maxy = max(ys) + 1

    lines = []
    for y in range(miny, maxy + 1):
        line = []
        for x in range(minx, maxx + 1):
            line.append('#' if (x, y) in points else '.')
        lines.append(''.join(line))
    return '\n'.join(lines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        rays = parse(stream)
        time = find_message_time(rays)
        points = advance(rays, time)
        result1 = points_to_string(points)
        result2 = time

    return (result1, result2)
