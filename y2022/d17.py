"""Advent of Code 2022

Day 17: Pyroclastic Flow

https://adventofcode.com/2022/day/17
"""
import logging  # noqa: F401
from functools import cache

from util import timing


VERTICAL_GAP = 3    # New rocks begin this far above the top of the tower ...
HORIZONTAL_GAP = 2  # ... and this far away from the left wall


# Rock cell coordinates are relative to each rock's bottom-left corner.
ROCKS = (
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        )
ROCK_WIDTHS = (4, 3, 3, 1, 2)
ROCK_HEIGHTS = (1, 3, 3, 4, 2)


def parse(stream) -> str:
    line = stream.readline().strip()
    result = tuple(1 if ch == '>' else -1 for ch in line)
    return result


def get_cells(rock, vx: int, vy: int) -> set:
    return {(x + vx, y + vy) for x, y in rock}


class Grid:
    def __init__(self, moves: tuple, width: int = 7):
        self.dropped = set()
        self.moves = moves
        self.width = width
        self.height = 0
        self.rocks = 0
        self.rounds = 0

    def drop_rock(self):
        index = self.rocks % len(ROCKS)
        rock = ROCKS[index]
        rockwidth = ROCK_WIDTHS[index]

        x = HORIZONTAL_GAP
        y = self.height + VERTICAL_GAP
        while y >= 0:
            # Shift left or right
            move = self.moves[self.rounds % len(self.moves)]
            self.rounds += 1

            x += move
            if x < 0 or x + rockwidth > self.width:
                # This move would go out of bounds, so reverse it.
                x -= move
            else:
                # Check for collisions
                cells = get_cells(rock, x, y)
                if cells & self.dropped:
                    x -= move

            # Move down
            y -= 1

            # Check for collisions
            cells = get_cells(rock, x, y)
            if y < 0 or cells & self.dropped:
                y += 1
                cells = get_cells(rock, x, y)
                break

        logging.debug((x, y))
        self.dropped |= cells
        self.rocks += 1
        self.height = max(self.height, y + ROCK_HEIGHTS[index])

    def drop_rocks(self, count: int):
        for i in range(count):
            self.drop_rock()

    def __str__(self) -> str:
        lines = []
        for y in range(self.height + 2, -1, -1):
            line = []
            for x in range(self.width):
                ch = '#' if (x, y) in self.dropped else '.'
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        moves = parse(stream)
        grid = Grid(moves)
        grid.drop_rocks(2022)
        result1 = grid.height

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
