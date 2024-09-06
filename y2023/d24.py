#!/usr/bin/env python
from collections import namedtuple
from fractions import Fraction
from itertools import combinations

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


def scale_iter(v, f):
    return tuple((x * f for x in v))


def num_leading_zeros(row: list) -> int:
    for i, n in enumerate(row):
        if n != 0:
            return i
    return i + 1


def get_non_echelon_row(matrix: list) -> int:
    prev = -1
    for i, row in enumerate(matrix):
        z = num_leading_zeros(row)
        if z == len(row):
            return None
        if z <= prev:
            return i
        prev = z
    return None


def eliminate(matrix: list) -> list:
    """Perform a Gaussian elimination on an augmented matrix.

    Return the list of values in the solution, or raise an exception if a
    unique solution cannot be found.
    """
    while True:
        matrix.sort(key=num_leading_zeros)
        i = get_non_echelon_row(matrix)
        if i is None:
            break
        j = num_leading_zeros(matrix[i])
        upper = matrix[i - 1]
        for i in range(i, len(matrix)):
            lead = matrix[i][j]
            if lead == 0:
                break
            factor = Fraction(0 - lead, upper[j])
            scaled = scale_iter(upper, factor)
            matrix[i] = tuple(map(lambda a, b: a + b, matrix[i], scaled))

    width = len(matrix[0]) - 1
    solution = [None] * width
    for row in reversed(matrix):
        z = num_leading_zeros(row)
        aug = row[width]
        for j in range(z + 1, width):
            aug -= row[j] * solution[j]
        solution[z] = Fraction(aug, row[z])
    return solution


def get_matrix_rows(a: Hail, b: Hail) -> list:
    ap, av = a
    bp, bv = b
    rhs = [
            bp.x * bv.y - bp.y * bv.x - ap.x * av.y + ap.y * av.x,
            bp.x * bv.z - bp.z * bv.x - ap.x * av.z + ap.z * av.x,
            bp.z * bv.y - bp.y * bv.z - ap.z * av.y + ap.y * av.z,
            ]
    return [
            [bv.y - av.y, av.x - bv.x, 0, ap.y - bp.y, bp.x - ap.x, 0, rhs[0]],
            [bv.z - av.z, 0, av.x - bv.x, ap.z - bp.z, 0, bp.x - ap.x, rhs[1]],
            [0, av.z - bv.z, bv.y - av.y, 0, bp.z - ap.z, ap.y - bp.y, rhs[2]],
            ]


def get_intercept(hails: list[Hail]) -> Hail:
    """Return a trajectory that can intercept all of the hailstones."""
    def sortkey(h): return h.point.x

    hails = list(sorted(hails, key=lambda x: x.point.x))
    a, b, c = hails[:3]
    matrix = []
    matrix.extend(get_matrix_rows(a, b))
    matrix.extend(get_matrix_rows(a, c))
    solution = eliminate(matrix)
    rounded = ([int(round(x)) for x in solution])
    return Hail(Point3(*rounded[:3]), Vector(*rounded[3:]))


def run(stream, test=False):
    if test:
        area_min = 7
        area_max = 27
    else:
        area_min = 200000000000000
        area_max = 400000000000000

    with timing("Part 1\n"):
        hails = parse_hail(stream)
        result1 = get_intersections_xy(hails, area_min, area_max)
    print(f"Result for Part 1 = {result1} \n")

    with timing("Part 2\n"):
        rock = get_intercept(hails)
        result2 = sum(rock.point)
    print(f"Result for Part 2 = {result2} \n")
    return (result1, result2)
