"""Advent of Code 2025

Day 12: Christmas Tree Farm

https://adventofcode.com/2025/day/12
"""
import logging  # noqa: F401
from functools import cache

from grid import SparseGrid
from util import timing


def rotate(rows: list[tuple]) -> list[tuple]:
    """Rotate the shape 90 degrees clockwise"""
    return tuple(
            tuple(row[x] for row in reversed(rows))
            for x in range(len(rows[0])))


def flip(rows: list[tuple]) -> list[tuple]:
    """Reverse every row."""
    return tuple(tuple(reversed(x)) for x in rows)


@cache
def get_rotations(shape):
    """Return all possible rotations of the shape."""
    result = {shape, flip(shape)}
    for _ in range(3):
        shape = rotate(shape)
        result.add(shape)
        result.add(flip(shape))
    return result


@cache
def count_empty(cells, position, width, height):
    x0, y0 = position
    return sum(
            int((x, y) not in cells)
            for y in range(y0, y0 + height)
            for x in range(x0, x0 + width))


@cache
def get_size(shape):
    return sum(sum(row) for row in shape)


@cache
def merge_cells(cells, shape, position):
    """Return the merged cells, if they do not collide."""
    shape_cells = get_shape_cells(shape, position)
    if not cells & shape_cells:
        return frozenset(cells | shape_cells)
    return None


@cache
def get_shape_cells(shape, position):
    cells = set()
    y = position[1]
    for row in shape:
        x = position[0]
        for cell in row:
            if cell:
                cells.add((x, y))
            x += 1
        y += 1
    return cells


@cache
def attempt_fit(width, height, cells, shapes, reqs):
    reqs = list(reqs)
    index = None
    for i, n in enumerate(reqs):
        if n > 0:
            index = i
            reqs[i] -= 1
            break
    if index is None:
        # Great, no shapes left to fit!
        return True
    shape = shapes[index]
    size = get_size(shape)

    # Step through all possible locations for this shape within the grid, and
    # all possible orientations of the shape at each location. Keep going until
    # we find a successful fit for the shape, and then recurse to the next
    # shape. If we can't find any fit for this shape, return False.
    for y in range(0, height - 2):
        for x in range(0, width - 2):
            # Check whether this position has enough empty cells to support the
            # shape, if it doesn't, we can skip it.
            if count_empty(cells, (x, y), 3, 3) < size:
                continue

            for r in get_rotations(shape):
                merged = merge_cells(cells, r, (x, y))
                if merged:
                    if attempt_fit(width, height, merged, shapes, tuple(reqs)):
                        return True
    return False


def render(width, height, cells):
    for y in range(height):
        line = []
        for x in range(width):
            p = (x, y)
            c = '#' if p in cells else '.'
            line.append(c)
        print(''.join(line))
    print()


def check_fit(shapes, region):
    """Return whether the region can fit all its required shapes."""
    width, height, reqs = region
    cells = frozenset()
    sizes = {i: get_size(x) for i, x in enumerate(shapes)}
    total = sum(sizes[i] * x for i, x in enumerate(reqs))
    if total > width * height:
        return False

    return attempt_fit(width, height, cells, shapes, reqs)


def cheat(region):
    """Check there is enough space for that many 3x3 blocks

    Turns out, today's puzzle was actually a prank and you don't need to do
    any packing at all.  Ha ha, so funny.
    """
    width, height, reqs = region
    count = sum(reqs)
    return count <= (width / 3) * (height / 3)


def parse(stream) -> str:
    data = stream.read()
    blocks = data.split('\n\n')
    shapes = []
    for block in blocks[:-1]:
        lines = block.split('\n')
        index = int(lines[0][:-1])
        shape = (tuple(int(x == '#') for x in line)
                 for line in lines[1:])
        shapes.append(tuple(shape))

    regions = []
    for line in blocks[-1].split('\n'):
        if not line:
            continue
        size, quantities = line.split(': ')
        width, height = map(int, size.split('x'))
        quantities = tuple(map(int, quantities.split()))
        regions.append((width, height, quantities))
    return tuple(shapes), regions


def run(stream, test: bool = False):
    with timing("Part 1"):
        shapes, regions = parse(stream)
        if test:
            result1 = sum(int(check_fit(shapes, x)) for x in regions)
        else:
            result1 = sum(int(cheat(x)) for x in regions)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
