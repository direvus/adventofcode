"""Advent of Code 2022

Day 14: Regolith Reservoir

https://adventofcode.com/2022/day/14
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self):
        self.source = (500, 0)
        self.rock = set()
        self.sand = set()
        self.maxy = 0

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            if line == '':
                break
            points = line.split(' -> ')
            start = tuple(int(x) for x in points[0].split(','))
            self.rock.add(start)
            for point in points[1:]:
                end = tuple(int(x) for x in point.split(','))
                x, y = start
                # Either vertical or horizontal
                vx = 0 if x == end[0] else 1 if x < end[0] else -1
                vy = 0 if y == end[1] else 1 if y < end[1] else -1
                while (x, y) != end:
                    x += vx
                    y += vy
                    self.rock.add((x, y))
                start = end
        self.maxy = max(p[1] for p in self.rock)

    def is_blocked(self, position: tuple) -> bool:
        return (position in self.rock or position in self.sand)

    def do_single_flow(self) -> tuple | None:
        """Calculate the final resting location of a single sand unit.

        Return the position that the new sand unit will rest in, or None if it
        will flow off the bottom edge of the grid.
        """
        x, y = self.source
        while y < self.maxy + 2:
            dest = None
            for point in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1)):
                if not self.is_blocked(point):
                    dest = point
                    break
            if dest is None:
                # No available moves, sand will rest here.
                return (x, y)
            x, y = dest

    def do_flow(self) -> int:
        """Flow sand until it leaves the grid.

        Continue adding new sand units to the grid until one of them falls off
        the bottom edge of the grid, then return the number of sand units that
        came to rest.
        """
        result = 0
        while True:
            p = self.do_single_flow()
            if p is None:
                return result
            else:
                self.sand.add(p)
                result += 1

    def count_sand(self) -> int:
        """Return the total number of cells that have sand."""
        return len(self.sand)


class FloorGrid(Grid):
    def is_blocked(self, position: tuple) -> bool:
        return (
                position in self.rock or
                position in self.sand or
                position[1] == self.maxy + 2)

    def do_flow(self) -> int:
        """Flow sand until it rests at the source.

        Continue adding new sand units to the grid until one of them has
        nowhere to move from the starting cell, then return the number of sand
        units that came to rest.
        """
        result = 0
        p = None
        while p != self.source:
            p = self.do_single_flow()
            self.sand.add(p)
            result += 1
        return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        result1 = grid.do_flow()

    with timing("Part 2"):
        grid2 = FloorGrid()
        grid2.rock = grid.rock
        grid2.maxy = grid.maxy

        result2 = grid2.do_flow()

    return (result1, result2)
