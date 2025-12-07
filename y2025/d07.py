"""Advent of Code 2025

Day 7: Laboratories

https://adventofcode.com/2025/day/7
"""
import logging  # noqa: F401

import grid
from util import timing


class Grid(grid.SparseGrid):
    def parse_cell(self, position, value):
        if value == 'S':
            self.start = position
        elif value == '^':
            self.cells.add(position)

    def count_splits(self):
        x, y = self.start
        cols = {x}
        splits = 0
        while y < self.height:
            new = set()
            for x in cols:
                if (x, y) in self.cells:
                    splits += 1
                    new.add(x - 1)
                    new.add(x + 1)
                else:
                    new.add(x)
            y += 1
            cols = new
        return splits


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        result1 = grid.count_splits()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
