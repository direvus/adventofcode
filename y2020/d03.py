"""Advent of Code 2020

Day 3: Toboggan Trajectory

https://adventofcode.com/2020/day/3
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self, stream):
        self.trees = set()
        self.height = 0
        self.width = 0

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            for x, ch in enumerate(line):
                if ch == '#':
                    self.trees.add((x, y))
            y += 1
        self.height = y + 1
        self.width = x + 1

    def count_trees_on_slope(self, across: int, down: int) -> int:
        x = 0
        y = 0
        result = 0
        while y < self.height:
            if (x, y) in self.trees:
                result += 1
            x = (x + across) % self.width
            y += down
        return result


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.count_trees_on_slope(3, 1)

    with timing("Part 2"):
        result2 = result1
        for args in ((1, 1), (5, 1), (7, 1), (1, 2)):
            result2 *= grid.count_trees_on_slope(*args)

    return (result1, result2)
