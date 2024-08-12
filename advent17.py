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
            (y, x, d, r): None
            for y in range(height)
            for x in range(width)
            for d in Direction
            for r in range(1, 4)
            if (y, x) != (0, 0)}
    nodes[(0, 0, direction, 0)] = 0
    dest = (height - 1, width - 1)
    run = 0
    heat = 0

    visited = {}

    while [k for k, v in nodes.items() if k[:2] == dest and v is None]:
        left, right = TURNS[direction]
        nbors = [
            (*move(pos, left), left, 1),
            (*move(pos, right), right, 1),
            ]

        if run < 3:
            nbors.append((*move(pos, direction), direction, run + 1))

        nbors = filter(lambda x: x in nodes, nbors)
        for y, x, d, r in nbors:
            dist = nodes[(y, x, d, r)]
            tile = rows[y][x]
            new = heat + tile
            if dist is None or dist > new:
                nodes[(y, x, d, r)] = new

        # DEBUG save off visited for viewing later
        visited[(*pos, direction, run)] = heat
        del nodes[(*pos, direction, run)]

        candidates = [
                (*k, v) for k, v in nodes.items()
                if v is not None]
        if not candidates:
            print("All nodes checked")
            break
        candidates.sort(key=lambda x: x[4])
        y, x, direction, run, heat = candidates[0]
        pos = (y, x)

    heats = [v for k, v in visited.items() if k[:2] == dest and v is not None]
    return min(heats)


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        rows.append([int(x) for x in line.strip()])

    # Part 1
    with timing("Part 1\n"):
        score = find_path(rows)
    print(f"Result for Part 1 = {score}\n")
