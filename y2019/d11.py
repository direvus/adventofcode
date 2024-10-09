"""Advent of Code 2019

Day 11: Space Police

https://adventofcode.com/2019/day/11
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def turn(direction: int, clockwise: bool = True) -> int:
    change = 1 if clockwise else -1
    return (direction + change) % 4


def move(position: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return tuple(x + v[i] for i, x in enumerate(position))


class Grid:
    def __init__(self):
        self.robot = Computer()
        self.position = (0, 0)
        self.direction = 0
        self.painted = set()

    def parse(self, stream):
        self.robot.parse(stream)

    def reset(self):
        self.robot.reset()
        self.position = (0, 0)
        self.direction = 0
        self.painted = set()

    def run(self):
        """Run the robot until it halts."""
        while not self.robot.halt:
            current = int(self.position in self.painted)
            self.robot.add_input(current)
            try:
                colour = next(self.robot.generate())
                rotation = next(self.robot.generate())

                if colour:
                    self.painted.add(self.position)
                else:
                    self.painted.discard(self.position)
                self.direction = turn(self.direction, rotation)
                self.position = move(self.position, self.direction)
            except StopIteration:
                pass

    def count_painted_panels(self) -> int:
        """Run the robot until it halts.

        Return the number of tiles that the robot painted at least once.
        """
        result = set()
        while not self.robot.halt:
            current = int(self.position in self.painted)
            self.robot.add_input(current)
            try:
                colour = next(self.robot.generate())
                rotation = next(self.robot.generate())

                if colour:
                    self.painted.add(self.position)
                else:
                    self.painted.discard(self.position)
                result.add(self.position)

                self.direction = turn(self.direction, rotation)
                self.position = move(self.position, self.direction)
            except StopIteration:
                pass
        return len(result)

    def to_string(self) -> str:
        """Return a string representation of the grid."""
        lines = []
        ys = {p[1] for p in self.painted}
        xs = {p[0] for p in self.painted}
        miny, maxy = min(ys), max(ys)
        minx, maxx = min(xs), max(xs)

        for y in range(miny, maxy + 1):
            line = []
            for x in range(minx, maxx + 1):
                ch = '#' if (x, y) in self.painted else ' '
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> Grid:
    g = Grid()
    g.parse(stream)
    return g


def run(stream, test: bool = False):
    if test:
        # There's really no way to test this one effectively, the puzzle did
        # not provide an example robot program, and I'm not going to write one
        # from scratch.
        return (0, 0)

    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.count_painted_panels()

    with timing("Part 2"):
        grid.reset()
        grid.painted.add((0, 0))
        grid.run()
        result2 = grid.to_string()

    return (result1, result2)
