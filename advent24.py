#!/usr/bin/env python
import argparse
import sys
from collections import namedtuple
from itertools import combinations, permutations

from rich import print

from util import timing


Line = namedtuple('line', ['a', 'b'])
Point3 = namedtuple('point', ['x', 'y', 'z'])
Vector = namedtuple('vector', ['x', 'y', 'z'])
Hail = namedtuple('hail', ['point', 'vector'])


def parse_hail(stream) -> list[Hail]:
    result = []
    for line in stream:
        line = line.strip()
        p, v = line.split(' @ ')
        point_ints = [int(x.strip()) for x in p.split(',')]
        vector_ints = [int(x.strip()) for x in v.split(',')]
        point = Point3(*point_ints)
        vector = Vector(*vector_ints)
        result.append(Hail(point, vector))
    return result


def get_intersection_xy(a: Hail, b: Hail) -> tuple | None:
    """Return the intersection in XY space of two hailstones.

    If the hailstones do not intersect at all (they are parallel) then return
    None.

    Otherwise, return a tuple containing the (x, y) location where they
    intersect.
    """
    assert a != b
    # There are no verticals in the input, so don't bother trying to handle
    # them.
    assert a.vector.x != 0 and b.vector.x != 0

    a_gradient = a.vector.y / a.vector.x
    b_gradient = b.vector.y / b.vector.x
    convergence = a_gradient - b_gradient
    if convergence == 0:
        return None
    assert convergence != 0

    ydist = b.point.y + (a.point.x - b.point.x) * b_gradient - a.point.y
    x = a.point.x + ydist / convergence
    y = a.point.y + (x - a.point.x) * a_gradient
    return x, y


def get_intersections_xy(
        hails: list[Hail], area_min: int, area_max: int) -> int:
    """Return the number of intersections between hailstones in XY.

    Only intersections that occur between `area_min` and `area_max` in the X
    and Y dimensions are counted.
    """
    count = 0
    for a, b in combinations(hails, 2):
        p = get_intersection_xy(a, b)
        if p is None:
            continue
        x, y = p
        # Disregard intersections in the past
        a_behind = x < a.point.x if a.vector.x > 0 else x > a.point.x
        b_behind = x < b.point.x if b.vector.x > 0 else x > b.point.x
        if a_behind or b_behind:
            continue
        # Disregard intersections outside the target area
        if x >= area_min and x <= area_max and y >= area_min and y <= area_max:
            count += 1
    return count


def advance_hail(hail: Hail, t: int) -> Hail:
    """Return the hailstone's position after `t` nanoseconds."""
    p = Point3(
            hail.point.x + t * hail.vector.x,
            hail.point.y + t * hail.vector.y,
            hail.point.z + t * hail.vector.z,
            )
    return Hail(p, hail.vector)


def cross(a: Vector, b: Vector) -> Vector:
    return Vector(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x)


def dot(a: Vector, b: Vector) -> int:
    return a.x * b.x + a.y * b.y + a.z * b.z


def intersects(a: Hail, b: Hail) -> bool:
    """Return whether two trajectories intersect."""
    p = Point3(
            a.point.x - b.point.x,
            a.point.y - b.point.y,
            a.point.z - b.point.z)
    return dot(cross(a.vector, b.vector), p) == 0


def intersects_all(line: Hail, hails: list[Hail]) -> bool:
    """Return whether the given line can intersect all the hail."""
    for h in hails:
        if not intersects(h, line):
            return False
    return True


def get_intercept(hails: list[Hail]) -> Hail:
    """Return a trajectory that can intercept all of the hailstones."""
    t1 = 1
    attempts = 500

    def sortkey(h): return h.point.z

    while t1 < attempts:
        frame1 = [advance_hail(x, t1) for x in hails]
        frame1.sort(key=sortkey)
        h1 = frame1.pop(0)

        for dt in range(1, attempts):
            frame2 = [advance_hail(x, dt) for x in frame1]
            frame2.sort(key=sortkey)
            h2 = frame2.pop(0)

            vector = Vector(
                    (h2.point.x - h1.point.x) / dt,
                    (h2.point.y - h1.point.y) / dt,
                    (h2.point.z - h1.point.z) / dt)
            line = Hail(h1.point, vector)
            if intersects_all(line, frame2):
                # Found it!
                return advance_hail(line, -t1)
        t1 += 1
    raise ValueError("No intercept found!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    args = parser.parse_args()

    if args.test:
        area_min = 7
        area_max = 27
    else:
        area_min = 200000000000000
        area_max = 400000000000000

    with timing("Part 1\n"):
        hails = parse_hail(sys.stdin)
        result = get_intersections_xy(hails, area_min, area_max)
    print(f"Result for Part 1 = {result} \n")

    with timing("Part 2\n"):
        rock = get_intercept(hails)
        result = sum(rock.point)
    print(f"Result for Part 2 = {result} \n")
