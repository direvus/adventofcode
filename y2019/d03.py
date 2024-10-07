"""Advent of Code 2019

Day 3: Crossed Wires

https://adventofcode.com/2019/day/3
"""
import logging  # noqa: F401
from collections import namedtuple

from util import timing


VECTORS = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
        }
P = namedtuple('P', ('x', 'y'))
L = namedtuple('L', ('a', 'b'))


def move(point: P, direction: str, length: int) -> P:
    return P(
            point.x + VECTORS[direction][0] * length,
            point.y + VECTORS[direction][1] * length,
            )


class Line:
    def __init__(self, a: P, b: P):
        self.a = a
        self.b = b

    @property
    def vertical(self) -> bool:
        return self.a.x == self.b.x

    @property
    def horizontal(self) -> bool:
        return self.a.y == self.b.y


def get_intersection(line1: Line, line2: Line) -> P | None:
    """Return the intersection of two lines.

    If the lines do not intersect at a single point (they are colinear, or
    disjoint) then return None.
    """
    if line1.vertical == line2.vertical:
        return None

    v = line1
    h = line2
    if not line1.vertical:
        v, h = h, v

    miny, maxy = sorted((v.a.y, v.b.y))
    if miny > h.a.y or maxy < h.a.y:
        return None
    minx, maxx = sorted((h.a.x, h.b.x))
    if minx > v.a.x or maxx < v.a.x:
        return None
    return P(v.a.x, h.a.y)


class Wire:
    def __init__(self):
        self.points = [P(0, 0)]

    def add_point(self, direction: str, length: int):
        new = move(self.points[-1], direction, length)
        self.points.append(new)

    def lines(self):
        for i in range(1, len(self.points)):
            yield Line(self.points[i - 1], self.points[i])

    def find_intersections(self, line: Line) -> set[P]:
        result = set()
        for segment in self.lines():
            p = get_intersection(segment, line)
            if p is not None:
                result.add(p)
        return result


def parse_wire(line: str) -> Wire:
    wire = Wire()
    for part in line.split(','):
        direction = part[0]
        length = int(part[1:])
        wire.add_point(direction, length)
    return wire


def parse(stream) -> list[Wire]:
    result = []
    for line in stream:
        line = line.strip()
        wire = parse_wire(line)
        result.append(wire)
    return result


def find_intersections(wire1: Wire, wire2: Wire) -> set[P]:
    result = set()
    for segment in wire1.lines():
        result |= wire2.find_intersections(segment)
    # The origin is an intersection but doesn't count.
    result -= {P(0, 0)}
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        wires = parse(stream)
        intersections = list(find_intersections(*wires))
        distances = map(lambda x: sum(abs(c) for c in x), intersections)
        result1 = min(distances)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
