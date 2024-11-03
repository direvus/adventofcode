"""Advent of Code 2021

Day 25: Sea Cucumber

https://adventofcode.com/2021/day/25
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self, stream):
        self.width = 0
        self.height = 0
        self.east = set()
        self.south = set()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            for x, ch in enumerate(line):
                p = (x, y)
                if ch == 'v':
                    self.south.add(p)
                elif ch == '>':
                    self.east.add(p)
            y += 1
        self.height = y
        self.width = x + 1

    def __str__(self):
        result = []
        for y in range(0, self.height):
            line = []
            for x in range(0, self.width):
                p = (x, y)
                if p in self.east:
                    ch = '>'
                elif p in self.south:
                    ch = 'v'
                else:
                    ch = '.'
                line.append(ch)
            result.append(''.join(line))
        return '\n'.join(result)

    def get_east(self, position):
        x, y = position
        x = (x + 1) % self.width
        return (x, y)

    def get_south(self, position):
        x, y = position
        y = (y + 1) % self.height
        return (x, y)

    def update(self) -> int:
        moves = 0
        new = set()
        blocked = self.east | self.south
        for p in self.east:
            target = self.get_east(p)
            if target in blocked:
                new.add(p)
            else:
                moves += 1
                new.add(target)
        self.east = new

        new = set()
        blocked = self.east | self.south
        for p in self.south:
            target = self.get_south(p)
            if target in blocked:
                new.add(p)
            else:
                moves += 1
                new.add(target)
        self.south = new
        return moves

    def update_until_stop(self):
        step = 0
        moves = 1
        while moves != 0:
            moves = self.update()
            step += 1
        return step


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid(stream)
        result1 = grid.update_until_stop()

    result2 = None

    return (result1, result2)
