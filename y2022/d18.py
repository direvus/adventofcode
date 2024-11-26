"""Advent of Code 2022

Day 18: Boiling Boulders

https://adventofcode.com/2022/day/18
"""
import logging  # noqa: F401
from collections import deque
from functools import cache

from util import timing, INF


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

    Each face is returned as a 6-tuple that describes the corner of the square
    closest to the origin in 3D space, and a vector that indicates which way
    the face is oriented (pointing away from the center of the cube):

    (x, y, z, vx, vy, vz)

    The collection of all 6 faces of the cube are returned as a set.
    """
    x, y, z = cube
    return {
            (x - 1, y - 1, z - 1,  -1, 0, 0),
            (x - 1, y - 1, z - 1,  0, -1, 0),
            (x - 1, y - 1, z - 1,  0, 0, -1),
            (x, y - 1, z - 1,  1, 0, 0),
            (x - 1, y, z - 1,  0, 1, 0),
            (x - 1, y - 1, z,  0, 0, 1),
            }


def get_bounding_box(cubes: tuple) -> tuple:
    """Return the bounding box that contains all cubes.

    This is returned as a 6-tuple of two corners of the minimal cuboid that
    contains all of the cubes.
    """
    minx = INF
    miny = INF
    minz = INF
    maxx = 0
    maxy = 0
    maxz = 0

    for x, y, z in cubes:
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if z < minz:
            minz = z
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
        if z > maxz:
            maxz = z
    return (minx, miny, minz, maxx, maxy, maxz)


def get_faced_cube(face: tuple) -> tuple:
    """Return the cube that this face immediately points toward."""
    x, y, z, vx, vy, vz = face
    return (
            x + (1 if vx >= 0 else 0),
            y + (1 if vy >= 0 else 0),
            z + (1 if vz >= 0 else 0),
            )


def get_exposed_faces(cubes: tuple) -> set:
    """Return all the cube faces that are exposed.

    We determine this by looking at faces that are not shared between any two
    cubes.

    Return the exposed faces as a set of tuples.
    """
    faces = set()
    for cube in cubes:
        faces |= get_faces(cube)

    result = set()
    for face in faces:
        x, y, z, vx, vy, vz = face
        opposite = (x, y, z, -vx, -vy, -vz)
        if opposite not in faces:
            result.add(face)
    return result


def get_exterior_faces(cubes: tuple) -> set:
    """Return all the cube faces that are exterior to the shape.

    We start with all of the exposed faces, and eliminate those that are
    internal to the shape, by running a fill.
    """
    cubes = set(cubes)
    faces = get_exposed_faces(cubes)
    bounds = get_bounding_box(cubes)
    internals = set()
    externals = set()
    result = set()

    for face in faces:
        start = get_faced_cube(face)
        q = deque()
        q.append(start)
        region = set()
        while q:
            p = q.pop()
            region.add(p)
            if p in internals:
                # This region has already been identified as internal.
                break
            if p in externals:
                # This region joins onto a region we've already identified as
                # external
                result.add(face)
                break
            x, y, z = p
            if (
                    x < bounds[0] or y < bounds[1] or z < bounds[2] or
                    x > bounds[3] or y > bounds[4] or z > bounds[5]):
                # This region extends outside the bounding box, so it is
                # external
                result.add(face)
                break

            # Visit all adjacent empty cubes
            adjacent = {
                    (x - 1, y, z),
                    (x + 1, y, z),
                    (x, y - 1, z),
                    (x, y + 1, z),
                    (x, y, z - 1),
                    (x, y, z + 1),
                    }
            for adj in adjacent - cubes - region:
                q.append(adj)
        if face in result:
            externals |= region
        else:
            internals |= region
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        cubes = parse(stream)
        result1 = len(get_exposed_faces(cubes))

    with timing("Part 2"):
        externals = get_exterior_faces(cubes)
        result2 = len(externals)

    return (result1, result2)
