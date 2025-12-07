"""Advent of Code 2025

Day 7: Laboratories

https://adventofcode.com/2025/day/7
"""
import logging  # noqa: F401
from collections import defaultdict

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

    def get_neighbours(self, position):
        x, y = position
        beams = {x - 1, x + 1}
        y = y + 1
        result = set()
        while y < self.height:
            for x in tuple(beams):
                if (x, y) in self.cells:
                    result.add((x, y))
                    beams.remove(x)
            y += 1
        return result

    def count_paths(self, node):
        if node in self.paths:
            return self.paths[node]
        neighbours = self.get_neighbours(node)
        count = (2 - len(neighbours))
        count += sum([self.count_paths(x) for x in neighbours])
        self.paths[node] = count
        return count

    def count_all_paths(self):
        self.paths = defaultdict(lambda: 0)

        # Find the first split from the start
        x, y = self.start
        y += 1
        while y < self.height:
            if (x, y) in self.cells:
                return self.count_paths((x, y))
            y += 1


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        result1 = grid.count_splits()

    with timing("Part 2"):
        result2 = grid.count_all_paths()

    return (result1, result2)
