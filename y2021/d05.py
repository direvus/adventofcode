"""Advent of Code 2021

Day 5: Hydrothermal Venture

https://adventofcode.com/2021/day/5
"""
import logging  # noqa: F401
from itertools import combinations

from util import timing


class Line:
    """A straight 2D line."""
    def __init__(self, a: tuple, b: tuple):
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f'{self.a} -> {self.b}'

    @property
    def vertical(self) -> bool:
        return self.a[0] == self.b[0]

    @property
    def horizontal(self) -> bool:
        return self.a[1] == self.b[1]

    @property
    def angle(self) -> int:
        """Return the angle of this line as a simplified integer value.

        Since lines can only be vertical, diagonal or horizontal in this
        puzzle, the return value is one of four possible options:

        0 - horizontal
        1 - diagonal top-left to bottom-right
        -1 - diagonal top-right to bottom-left
        2 - vertical
        """
        if self.horizontal:
            return 0
        if self.vertical:
            return 2
        left, right = sorted((self.a, self.b))
        if left[1] < right[1]:
            return 1
        else:
            return -1

    @property
    def length(self) -> int:
        if self.vertical:
            return abs(self.b[1] - self.a[1])
        return abs(self.b[0] - self.a[0])

    @property
    def points(self) -> set:
        result = set()
        if self.vertical:
            x = self.a[0]
            miny, maxy = sorted((self.a[1], self.b[1]))
            for y in range(miny, maxy + 1):
                result.add((x, y))
        elif self.horizontal:
            y = self.a[1]
            minx, maxx = sorted((self.a[0], self.b[0]))
            for x in range(minx, maxx + 1):
                result.add((x, y))
        else:
            left, right = sorted((self.a, self.b))
            step = self.angle
            y = left[1]
            for x in range(left[0], right[0] + 1):
                result.add((x, y))
                y += step
        return result

    @property
    def x_intercept(self) -> int | None:
        if self.horizontal:
            return None
        if self.vertical:
            return self.a[0]
        return self.a[0] - (self.angle * self.a[1])


def get_line_intersection(line1: Line, line2: Line) -> set:
    """Return the intersection of two lines.

    Lines are allowed to be horizontal, vertical, or on a 45 degree diagonal.

    Return the set of points that belong to both lines.
    """
    if line1.angle == line2.angle:
        # These lines share the same orientation, so they could overlap on
        # multiple points. We can skip calculating the overlap if the lines are
        # not equal on their fixed axis.
        if line1.vertical:
            if line1.a[0] != line2.a[0]:
                return set()
            return line1.points & line2.points
        if line1.horizontal:
            if line1.a[1] != line2.a[1]:
                return set()
            return line1.points & line2.points
        if line1.x_intercept != line2.x_intercept:
            return set()
        return line1.points & line2.points

    # The lines have different orientations, so there is either a single point
    # intersection, or none at all. If they are vertical and horizontal, maths
    # it out, if there is a diagonal in the mix, enumerate all points and take
    # the common set.
    if {line1.angle, line2.angle} == {0, 2}:
        v = line1
        h = line2
        if not line1.vertical:
            v, h = h, v

        miny, maxy = sorted((v.a[1], v.b[1]))
        if miny > h.a[1] or maxy < h.a[1]:
            return set()
        minx, maxx = sorted((h.a[0], h.b[0]))
        if minx > v.a[0] or maxx < v.a[0]:
            return set()
        return {(v.a[0], h.a[1])}
    return line1.points & line2.points


def parse(stream) -> list[Line]:
    result = []
    for line in stream:
        line = line.strip()
        a, b = line.split(' -> ')
        a = tuple(int(x) for x in a.split(','))
        b = tuple(int(x) for x in b.split(','))
        result.append(Line(a, b))
    return result


def count_overlaps_vh(lines) -> int:
    overlaps = set()
    lines = filter(lambda x: x.horizontal or x.vertical, lines)
    for a, b in combinations(lines, 2):
        overlaps |= get_line_intersection(a, b)
    return len(overlaps)


def count_overlaps(lines) -> int:
    overlaps = set()
    for a, b in combinations(lines, 2):
        overlaps |= get_line_intersection(a, b)
    return len(overlaps)


def run(stream, test: bool = False):
    with timing("Part 1"):
        lines = parse(stream)
        result1 = count_overlaps_vh(lines)

    with timing("Part 2"):
        result2 = count_overlaps(lines)

    return (result1, result2)
