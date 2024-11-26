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
        self.history = []

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

        self.dropped |= cells
        self.rocks += 1
        self.height = max(self.height, y + ROCK_HEIGHTS[index])
        self.history.append((x, self.height))

    def drop_rocks(self, count: int):
        for i in range(count):
            self.drop_rock()

    def find_cycle(self, rock: int):
        self.dropped = set()
        self.height = 0
        self.rocks = 0
        self.rounds = 0
        self.history = []
        step = len(ROCKS)
        while True:
            self.drop_rock()
            if len(self.history) < 100 or self.rocks % step != rock:
                continue

            index = len(self.history) - step
            pattern = tuple(x[0] for x in self.history[index:])
            i = index - step
            while i >= 0:
                xs = tuple(x[0] for x in self.history[i: i + step])
                if xs == pattern:
                    # Check the previous two iterations of this cycle
                    cycle = index - i
                    if i < cycle * 2:
                        # Not enough history to check two full cycles
                        break
                    i1 = i - cycle
                    i2 = i - cycle * 2
                    x1 = tuple(x[0] for x in self.history[i1: i1 + step])
                    x2 = tuple(x[0] for x in self.history[i2: i2 + step])
                    if x1 == pattern and x2 == pattern:
                        return (i, index)
                i -= step

    def predict_height(self, rocks: int):
        i1, i2 = self.find_cycle(rocks % len(ROCKS))
        h1 = self.history[i1][1]
        h2 = self.history[i2][1]
        growth = h2 - h1
        cycle = i2 - i1
        logging.debug(f'height grows {growth} per {cycle} rocks from {i2}')

        diff = rocks - i2 - 1
        cycles, remain = divmod(diff, cycle)
        logging.debug(
                f'require {diff} more rocks = {cycles} cycles '
                f'and {remain} remaining')

        height = h2 + growth * cycles
        i = i2 + cycle * cycles
        logging.debug(f'height will be {height} at rock {i}')

        h = self.history[i1 + remain][1] - h1
        logging.debug(f'tower grew {h} over {remain} drops')

        return height + h

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
        result2 = grid.predict_height(1000000000000)

    return (result1, result2)
