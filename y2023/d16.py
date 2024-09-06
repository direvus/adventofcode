#!/usr/bin/env python
from util import timing, Direction


VECTORS = {
        Direction.NORTH: (-1,  0),
        Direction.SOUTH:  (1,  0),
        Direction.EAST:   (0,  1),
        Direction.WEST:   (0, -1),
        }
MIRRORS = {
        '\\': {
            Direction.NORTH: Direction.WEST,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST:  Direction.SOUTH,
            Direction.WEST:  Direction.NORTH,
            },
        '/': {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.EAST:  Direction.NORTH,
            Direction.WEST:  Direction.SOUTH,
            },
        }
SPLITTERS = {
        #    ({directions affected}, (output directions))
        '|': (
            {Direction.EAST, Direction.WEST},
            (Direction.NORTH, Direction.SOUTH),
            ),
        '-': (
            {Direction.NORTH, Direction.SOUTH},
            (Direction.EAST, Direction.WEST),
            ),
        }


def in_bounds(rows: list, position: tuple[int]) -> bool:
    y, x = position
    return y >= 0 and y < len(rows) and x >= 0 and x < len(rows[0])


def move(position: tuple[int], direction: Direction) -> tuple[int]:
    v = VECTORS[direction]
    return (position[0] + v[0], position[1] + v[1])


def run_beam(
        rows: list,
        tiles: dict,
        position: tuple[int],
        direction: Direction,
        ) -> None:
    while in_bounds(rows, position):
        if direction in tiles.get(position, set()):
            # A beam has already trod this path, exit.
            return
        tiles.setdefault(position, set()).add(direction)

        y, x = position
        tile = rows[y][x]

        match tile:
            case '\\' | '/':
                direction = MIRRORS[tile][direction]
            case '|' | '-':
                if direction in SPLITTERS[tile][0]:
                    directions = SPLITTERS[tile][1]
                    direction = directions[0]
                    run_beam(rows, tiles, position, directions[1])

        position = move(position, direction)


def count_tiles(
        rows: list,
        position: tuple[int],
        direction: Direction,
        ) -> None:
    tiles = {}
    run_beam(rows, tiles, position, direction)
    return len(tiles)


def run(stream, test=False):
    rows = []
    for line in stream:
        rows.append(line.strip())

    # Part 1
    with timing("Part 1"):
        count = count_tiles(rows, (0, 0), Direction.EAST)
    print(f"Result for Part 1 = {count}\n")

    # Part 2
    with timing("Part 2"):
        results = []
        width = len(rows[0])
        height = len(rows)
        for x in range(width):
            results.append(count_tiles(rows, (0, x), Direction.SOUTH))
            results.append(count_tiles(rows, (height - 1, x), Direction.NORTH))
        for y in range(height):
            results.append(count_tiles(rows, (y, 0), Direction.EAST))
            results.append(count_tiles(rows, (y, width - 1), Direction.WEST))
        result = max(results)
    print(f"Result for Part 2 = {result}\n")
    return (count, result)
