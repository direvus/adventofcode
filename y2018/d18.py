"""Advent of Code 2018

Day 18: Settlers of The North Pole

https://adventofcode.com/2018/day/18
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self, size: int = 50):
        self.size = size
        self.woods = set()
        self.yards = set()

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            for x, ch in enumerate(line):
                if ch == '#':
                    self.yards.add((x, y))
                elif ch == '|':
                    self.woods.add((x, y))
            y += 1
        return stream.readline().strip()

    def update(self):
        newwoods = set()
        newyards = set()

        for y in range(self.size):
            for x in range(self.size):
                p = (x, y)
                adj = {
                        (x - 1, y - 1),
                        (x - 1, y),
                        (x - 1, y + 1),
                        (x + 1, y - 1),
                        (x + 1, y),
                        (x + 1, y + 1),
                        (x, y - 1),
                        (x, y + 1),
                        }
                if p in self.woods:
                    yards = len(self.yards & adj)
                    if yards > 2:
                        newyards.add(p)
                    else:
                        newwoods.add(p)
                elif p in self.yards:
                    woods = len(self.woods & adj)
                    yards = len(self.yards & adj)
                    if woods > 0 and yards > 0:
                        newyards.add(p)
                else:
                    woods = len(self.woods & adj)
                    if woods > 2:
                        newwoods.add(p)
        self.woods = newwoods
        self.yards = newyards

    def run(self, count: int):
        for i in range(count):
            self.update()

    @property
    def total_resource(self) -> int:
        return len(self.woods) * len(self.yards)

    def to_string(self) -> str:
        lines = []
        for y in range(self.size):
            line = []
            for x in range(self.size):
                p = (x, y)
                if p in self.woods:
                    line.append('|')
                elif p in self.yards:
                    line.append('#')
                else:
                    line.append(' ')
            lines.append(''.join(line))
        return '\n'.join(lines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        size = 10 if test else 50
        grid = Grid(size)
        grid.parse(stream)
        grid.run(10)
        result1 = grid.total_resource

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
