#!/usr/bin/env python
import sys

from util import timing, Direction


VECTORS = {
        Direction.NORTH: (-1,  0),
        Direction.SOUTH:  (1,  0),
        Direction.EAST:   (0,  1),
        Direction.WEST:   (0, -1),
        }
TURNS = {
        # facing direction: (left turn, right turn)
        Direction.EAST: (Direction.NORTH, Direction.SOUTH),
        Direction.WEST: (Direction.SOUTH, Direction.NORTH),
        Direction.NORTH: (Direction.WEST, Direction.EAST),
        Direction.SOUTH: (Direction.EAST, Direction.WEST),
        }


def in_bounds(height: int, width: int, position: tuple[int]) -> bool:
    y, x = position
    return y >= 0 and y < height and x >= 0 and x < width


def move(position: tuple[int], direction: Direction) -> tuple[int]:
    v = VECTORS[direction]
    return (position[0] + v[0], position[1] + v[1])


def find_path(rows: list) -> int:
    pos = (0, 0)
    height = len(rows)
    width = len(rows[0])
    direction = Direction.EAST
    nodes = {
            (y, x, d): (None, 0)
            for y in range(height)
            for x in range(width)
            for d in Direction}
    nodes[(0, 0, direction)] = (0, 0)
    dest = (height - 1, width - 1)
    run = 0
    heat = 0

    visited = {}

    while pos != dest:
        print(f"At {pos} with heat {heat} heading {direction} for {run}")
        left, right = TURNS[direction]
        nbors = [
            (*move(pos, left), left),
            (*move(pos, right), right),
            ]

        if run < 3:
            nbors.append((*move(pos, direction), direction))

        nbors = filter(lambda x: x in nodes, nbors)
        for y, x, d in nbors:
            dist = nodes[(y, x, d)][0]
            tile = rows[y][x]
            new = heat + tile
            if dist is None or dist > new:
                r = run + 1 if d == direction else 0
                nodes[(y, x, d)] = (new, r)

        # DEBUG save off visited for viewing later
        visited[pos] = heat
        del nodes[(*pos, direction)]

        candidates = [
                (*k, *v) for k, v in nodes.items()
                if v[0] is not None]
        candidates.sort(key=lambda x: x[3])
        y, x, direction, heat, run = candidates[0]
        pos = (y, x)

    for y in range(height):
        row = []
        for x in range(width):
            if (y, x) in visited:
                row.append(f"{visited[(y, x)]:3d}")
            else:
                row.append('   ')
        print(' '.join(row))

    return heat


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        rows.append([int(x) for x in line.strip()])

    # Part 1
    with timing("Part 1\n"):
        score = find_path(rows)
    print(f"Result for Part 1 = {score}\n")
