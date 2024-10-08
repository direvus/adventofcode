"""Advent of Code 2019

Day 3: Crossed Wires

https://adventofcode.com/2019/day/3
"""
import logging  # noqa: F401
from collections import defaultdict, namedtuple

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
    """A straight 2D line constrained to vertical or horizontal."""
    def __init__(self, a: P, b: P):
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f'({self.a.x},{self.a.y}) -> ({self.b.x},{self.b.y})'

    @property
    def vertical(self) -> bool:
        return self.a.x == self.b.x

    @property
    def horizontal(self) -> bool:
        return self.a.y == self.b.y

    @property
    def length(self) -> int:
        if self.vertical:
            return abs(self.b.y - self.a.y)
        return abs(self.b.x - self.a.x)

    def contains(self, point: P) -> bool:
        return point_on_line(self, point)

    def get_steps_to_point(self, point: P) -> int:
        """Return the number of steps along this line to the point.

        The result only makes sense if the point actually lies on the line, and
        this function doesn't check whether it does.
        """
        axis = 1 if self.vertical else 0
        start = self.a[axis]
        value = point[axis]
        return abs(value - start)


def get_line_intersection(line1: Line, line2: Line) -> P | None:
    """Return the simple intersection of two lines.

    If the lines have no intersection, or they intersect at multiple points
    (colinear), then return None.
    """
    if line1.vertical == line2.vertical:
        # Both vertical, or both horizontal, so no simple intersection.
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


def point_on_line(line: Line, point: P) -> bool:
    """Return whether a point lies on a line."""
    if line.vertical:
        miny, maxy = sorted((line.a.y, line.b.y))
        return line.a.x == point.x and miny <= point.y and maxy >= point.y
    else:
        minx, maxx = sorted((line.a.x, line.b.x))
        return line.a.y == point.y and minx <= point.x and maxx >= point.x


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
            p = get_line_intersection(segment, line)
            if p is not None:
                result.add(p)
        return result

    def update_steps(self, points: set[P], result: dict):
        total = 0
        for segment in self.lines():
            for p in points:
                if segment.contains(p):
                    steps = total + segment.get_steps_to_point(p)
                    result[p] += steps
            total += segment.length


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


def find_fewest_steps_intersection(
        wire1: Wire, wire2: Wire, points: set[P]) -> int:
    steps = defaultdict(lambda: 0)
    wire1.update_steps(points, steps)
    wire2.update_steps(points, steps)
    return min(steps.values())


def run(stream, test: bool = False):
    with timing("Part 1"):
        wires = parse(stream)
        intersections = list(find_intersections(*wires))
        distances = map(lambda x: sum(abs(c) for c in x), intersections)
        result1 = min(distances)

    with timing("Part 2"):
        result2 = find_fewest_steps_intersection(*wires, intersections)

    return (result1, result2)
