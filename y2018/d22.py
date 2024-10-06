"""Advent of Code 2018

Day 22: Mode Maze

https://adventofcode.com/2018/day/22
"""
import logging  # noqa: F401

from util import timing


TYPES = '.=|'


class Grid:
    def __init__(self, depth: int, target: tuple):
        self.depth = depth
        self.target = target
        self.levels = {}

    def get_index(self, location: tuple) -> int:
        if location == (0, 0) or location == self.target:
            return 0
        x, y = location
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return self.get_level((x - 1, y)) * self.get_level((x, y - 1))

    def get_level(self, location: tuple) -> int:
        if location in self.levels:
            return self.levels[location]
        index = self.get_index(location)
        level = (index + self.depth) % 20183
        self.levels[location] = level
        return level

    def get_type(self, location: tuple) -> int:
        return self.get_level(location) % 3

    def get_risk(self) -> int:
        total = 0
        for x in range(self.target[0] + 1):
            for y in range(self.target[1] + 1):
                total += self.get_type((x, y))
        return total


def parse(stream) -> Grid:
    line = stream.readline().strip()
    depth = int(line.split()[-1])

    line = stream.readline().strip()
    target = tuple(int(x) for x in line.split()[-1].split(','))
    return Grid(depth, target)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.get_risk()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
