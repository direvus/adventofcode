"""Advent of Code 2022

Day 18: Boiling Boulders

https://adventofcode.com/2022/day/18
"""
import logging  # noqa: F401
from collections import Counter
from functools import cache

from util import timing


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        coords = (int(x) for x in line.split(','))
        result.append(tuple(coords))
    return result


@cache
def get_faces(cube: tuple) -> set:
    """Get the faces of a cube.

    Each face is returned as a 6-tuple that describes two corners of a square
    in 3D space:

    (x1, y1, z1, x2, y2, z2)

    The collection of all 6 faces of the cube are returned as a set.
    """
    x, y, z = cube
    return {
            (x - 1, y - 1, z - 1, x - 1, y, z),
            (x, y - 1, z - 1, x, y, z),
            (x - 1, y - 1, z - 1, x, y - 1, z),
            (x - 1, y, z - 1, x, y, z),
            (x - 1, y - 1, z - 1, x, y, z - 1),
            (x - 1, y - 1, z, x, y, z),
            }


def get_exposed_faces(cubes: tuple) -> set:
    """Return all the cube faces that are exposed.

    We determine this by looking at faces that are not shared between any two
    cubes.

    Return the exposed faces as a set of tuples.
    """
    counter = Counter()
    for cube in cubes:
        counter.update(get_faces(cube))

    return set(face for face, count in counter.items() if count == 1)


def run(stream, test: bool = False):
    with timing("Part 1"):
        cubes = parse(stream)
        result1 = len(get_exposed_faces(cubes))

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
