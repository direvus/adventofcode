"""Advent of Code 2025

Day 4: Printing Department

https://adventofcode.com/2025/day/4
"""
import logging  # noqa: F401

import grid
from util import timing


class Grid(grid.Grid):
    def parse_cell(self, position, value):
        return 1 if value == '@' else 0

    def is_accessible(self, cell):
        if not self.get_value(cell):
            return False
        neighbours = len({x for x in self.get_surround(cell) if self.get_value(x)})
        return neighbours < 4

    def count_accessible(self):
        return sum([
            int(self.is_accessible(x))
            for x in self.iter_cells()])


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        result1 = grid.count_accessible()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
