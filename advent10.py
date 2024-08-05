#!/usr/bin/env python
import sys
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


# These exit directions are set up so that for corner nodes, the first exit is
# in the clockwise direction of travel, and the second exit is in the
# anti-clockwise direction.
PIPES = {
        '|': (Direction.NORTH, Direction.SOUTH),
        '-': (Direction.WEST, Direction.EAST),
        'L': (Direction.NORTH, Direction.EAST),
        'J': (Direction.WEST, Direction.NORTH),
        '7': (Direction.SOUTH, Direction.WEST),
        'F': (Direction.EAST, Direction.SOUTH),
        }

# Pipe glyphs with connections to the:
NORTH = set('|LJ')
SOUTH = set('|7F')
EAST = set('-LF')
WEST = set('-J7')


def traverse(grid: list, vector: tuple) -> tuple:
    """Move one grid cell along the path.

    The vector is a tuple of (row, col, direction), representing the current
    position on the grid and the direction of facing.

    The return value is in the same format, giving the position of the next
    grid cell and the direction of the next exit from that cell.
    """
    row, col, direction = vector
    if direction == Direction.NORTH:
        row -= 1
        opposite = Direction.SOUTH
    elif direction == Direction.SOUTH:
        row += 1
        opposite = Direction.NORTH
    elif direction == Direction.EAST:
        col += 1
        opposite = Direction.WEST
    else:
        col -= 1
        opposite = Direction.EAST

    glyph = grid[row][col]
    pipe = PIPES[glyph]
    newdir = pipe[0] if opposite == pipe[1] else pipe[1]
    return (row, col, newdir)


if __name__ == '__main__':
    grid = []
    i = 0
    start = None
    home = None
    for line in sys.stdin:
        line = line.strip()
        if 'S' in line:
            j = line.index('S')
            start = (i, j)
            options = set(PIPES.keys())
            if i > 0 and grid[i - 1][j] in SOUTH:
                options &= NORTH
            else:
                options -= NORTH
            if j > 0 and line[j - 1] in EAST:
                options &= WEST
            else:
                options -= WEST
            if j < len(line) - 1 and line[j + 1] in WEST:
                options &= EAST
            else:
                options -= EAST
            if len(options) != 1:
                raise ValueError(f"Home has too many options: {options}")
            home = options.pop()
            line = line.replace('S', home)
        grid.append(line)
        i += 1

    height = len(grid)
    width = len(grid[0])

    # Part 1
    steps = 0
    a = (start[0], start[1], PIPES[home][0])
    b = (start[0], start[1], PIPES[home][1])
    while steps == 0 or a[:2] != b[:2]:
        a = traverse(grid, a)
        b = traverse(grid, b)
        steps += 1
    print(f"{steps} steps to reach the farthest tile")

    # Part 2 - tiles enclosed by the loop.
    #
    # First we'll traverse the whole loop and collect all the points along it.
    v = (start[0], start[1], PIPES[home][0])
    nodes = [start]
    while v[:2] != start or len(nodes) == 1:
        v = traverse(grid, v)
        node = v[:2]
        nodes.append(node)

    # Now we will scan all tiles, row by row. On each row we start "outside"
    # the loop. Each time we cross over the pipes we flip between "inside" and
    # "outside". Running along the pipes doesn't flip the state, but we have to
    # be careful about these two special cases:
    #
    #     |            |
    #     L---7    F---J
    #         |    |
    count = 0
    cross_corner = None
    for i in range(height):
        inside = False
        for j in range(width):
            node = (i, j)
            if node in nodes:
                glyph = grid[i][j]
                if glyph in {'|', cross_corner}:
                    inside = not inside
                    cross_corner = None
                elif glyph == 'L':
                    cross_corner = '7'
                elif glyph == 'F':
                    cross_corner = 'J'
            elif inside:
                count += 1
    print(f"{count} internal tiles")
