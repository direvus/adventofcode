"""grid.py

Utility module for a two-dimensional grid system.

These grids all use a two-dimensional Cartesian (X, Y) coordinate system, with
X values increasing to the right and Y values increasing downwards.
"""
from operator import add


FACING = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def in_bound(width: int, height: int, position: tuple) -> bool:
    return (
            position[0] >= 0 and position[0] < width and
            position[1] >= 0 and position[1] < height)


def get_adjacent(position: tuple) -> set:
    """Return all cells that are adjacent to `position`.

    In this case, adjacent means horizontally or vertically adjacent.
    """
    x, y = position
    return {
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y),
            }


def move(position: tuple, direction: int, count: int = 1) -> tuple:
    vector = (v * count for v in VECTORS[direction])
    return tuple(map(add, position, vector))


def turn(direction: int, steps: int = 1) -> int:
    """Return a new direction rotated `steps` times 90 degrees clockwise."""
    return (direction + steps) % 4


class Grid:
    """A two-dimensional, dense, bounded grid system.

    Intended for use when the grid contains a value for every cell.
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []

    def parse_cell(self, position: tuple, value: str | int):
        self.cells[position[1]][position[0]] = value

    def parse(self, stream):
        y = 0
        for line in stream:
            for x, ch in enumerate(line.strip()):
                self.parse_cell((x, y), ch)
            y += 1
        self.width = x + 1
        self.height = y

    def in_bound(self, position):
        return in_bound(self.width, self.height, position)

    def get_adjacent(self, position):
        return {x for x in get_adjacent(position) if self.in_bound(x)}


class SparseGrid(Grid):
    """A two-dimensional, sparse, bounded grid system.

    Intended for use when the grid contains a substantial amount of empty
    space, we only store values for the non-empty cells.
    """
    def __init__(self):
        super().__init__()
        self.cells = set()

    def parse_cell(self, position: tuple, value: str | int):
        if value == '#':
            self.cells.add(position)


class InfiniteGrid(SparseGrid):
    """A two-dimensional, sparse, infinite grid system.

    Intended for use when the grid contains a substantial amount of empty
    space and has no boundary.
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = set()

    def in_bound(self, position: tuple) -> bool:
        return True

    def get_adjacent(self, position):
        return get_adjacent(position)
