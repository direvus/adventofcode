"""Advent of Code 2024

Day 8: Resonant Collinearity

https://adventofcode.com/2024/day/8
"""
import logging  # noqa: F401
from collections import defaultdict
from itertools import combinations
from operator import add, sub

from util import timing


class Grid:
    def __init__(self):
        self.antennae = defaultdict(set)

    def parse(self, stream):
        y = 0
        for line in stream:
            for x, ch in enumerate(line.strip()):
                if ch != '.':
                    self.antennae[ch].add((x, y))
            y += 1
        self.height = y
        self.width = x + 1
        return self

    def in_bounds(self, position) -> bool:
        x, y = position
        return (x >= 0 and y >= 0 and x < self.width and y < self.height)

    def get_antinodes_pair(self, a, b):
        diff = tuple(map(sub, b, a))
        return {
                tuple(map(add, b, diff)),
                tuple(map(sub, a, diff)),
                }

    def get_antinodes(self):
        result = set()
        for key, antennae in self.antennae.items():
            for a, b in combinations(antennae, 2):
                antinodes = self.get_antinodes_pair(a, b)
                result.update(antinodes)
        return {x for x in result if self.in_bounds(x)}

    def get_harmonics_pair(self, a, b):
        result = {a}
        diff = tuple(map(sub, b, a))
        pos = tuple(map(add, a, diff))
        while self.in_bounds(pos):
            result.add(pos)
            pos = tuple(map(add, pos, diff))

        pos = tuple(map(sub, a, diff))
        while self.in_bounds(pos):
            result.add(pos)
            pos = tuple(map(sub, pos, diff))
        return result

    def get_harmonics(self):
        result = set()
        for key, antennae in self.antennae.items():
            for a, b in combinations(antennae, 2):
                nodes = self.get_harmonics_pair(a, b)
                result.update(nodes)
        return result


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        result1 = len(grid.get_antinodes())

    with timing("Part 2"):
        result2 = len(grid.get_harmonics())

    return (result1, result2)
