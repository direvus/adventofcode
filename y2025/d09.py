"""Advent of Code 2025

Day 9: Movie Theatre

https://adventofcode.com/2025/day/9
"""
import logging  # noqa: F401
from itertools import combinations

import grid
from util import get_euclidean_distance, timing


def get_area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


class Grid(grid.SparseGrid):
    def parse(self, stream):
        for line in stream:
            x, y = map(int, line.split(','))
            self.cells.add((x, y))

    def find_largest_rect(self):
        areas = [
                get_area(a, b)
                for a, b in combinations(self.cells, 2)]
        areas.sort()
        return areas[-1]


def parse(stream) -> str:
    grid = Grid()
    grid.parse(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_largest_rect()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
