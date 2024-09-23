"""Advent of Code 2017

Day 22: Sporifica Virus

https://adventofcode.com/2017/day/22
"""
import logging  # noqa: F401

from util import timing


DIRECTIONS = ('U', 'R', 'D', 'L')
VECTORS = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
        }


def move(position: tuple, direction: str) -> tuple:
    vy, vx = VECTORS[direction]
    return (position[0] + vy, position[1] + vx)


def turn(direction: str, count: int = 1) -> str:
    """Change direction by `count` increments of 90 degrees clockwise."""
    index = DIRECTIONS.index(direction)
    index = (index + count) % 4
    return DIRECTIONS[index]


class Grid:
    current: tuple[int, int]
    direction: str
    infected: set

    def __init__(self):
        self.current = (0, 0)
        self.direction = 'U'
        self.infected = set()

    def do_burst(self) -> 0 | 1:
        """Do one burst of the virus carrier.

        Return the number of nodes that were infected by this burst (either 0
        or 1).
        """
        result = 0
        infected = self.current in self.infected
        turns = 1 if infected else -1
        self.direction = turn(self.direction, turns)
        if infected:
            self.infected.remove(self.current)
        else:
            self.infected.add(self.current)
            result = 1
        self.current = move(self.current, self.direction)
        return result

    def do_bursts(self, count: int) -> int:
        """Do multiple bursts of the virus carrier.

        Return the total number of cells that were infected by the burst
        activity.
        """
        result = 0
        for i in range(count):
            result += self.do_burst()
        return result

    def to_string(self) -> str:
        result = []
        ys = list(x[0] for x in self.infected)
        xs = list(x[1] for x in self.infected)
        ys.sort()
        xs.sort()
        miny, maxy = ys[0], ys[-1]
        minx, maxx = xs[0], xs[-1]

        for y in range(miny - 1, maxy + 2):
            row = []
            for x in range(minx - 1, maxx + 2):
                infected = (y, x) in self.infected
                current = (y, x) == self.current
                if current:
                    ch = '*' if infected else '_'
                else:
                    ch = '#' if infected else '.'
                row.append(ch)
            result.append(''.join(row))
        result.append('')
        return '\n'.join(result)


def parse(stream) -> Grid:
    grid = Grid()
    y = 0
    length = None
    for line in stream:
        line = line.strip()
        for x, ch in enumerate(line):
            if ch == '#':
                grid.infected.add((y, x))
        if length is None:
            length = len(line)
            # Finding the middle point requires an odd number of cells
            assert length % 2 != 0
            mid = length // 2
            grid.current = (mid, mid)
        y += 1
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.do_bursts(10_000)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
