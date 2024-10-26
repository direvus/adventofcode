"""Advent of Code 2021

Day 11: Dumbo Octopus

https://adventofcode.com/2021/day/11
"""
import logging  # noqa: F401
from collections import deque

from util import timing


class Grid:
    def __init__(self, stream=''):
        self.height = 0
        self.width = 0
        self.values = []
        self.total_flashes = 0
        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            row = []
            for x, ch in enumerate(line):
                row.append(int(ch))
            self.values.append(row)
        self.height = len(self.values)
        self.width = x + 1

    def bump(self, position: tuple) -> int:
        """Increase the value of a cell and return the new value."""
        x, y = position
        self.values[y][x] += 1
        return self.values[y][x]

    def get_value(self, position: tuple):
        x, y = position
        return self.values[y][x]

    def set_value(self, position: tuple, value: int):
        x, y = position
        self.values[y][x] = 0

    def get_adjacent(self, position: tuple) -> set:
        x, y = position
        adjacent = (
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1))

        def filterfunc(p):
            x, y = p
            return (
                    x >= 0 and x < self.width and
                    y >= 0 and y < self.height)
        return set(filter(filterfunc, adjacent))

    def do_step(self) -> int:
        q = deque()
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                value = self.bump(p)
                if value > 9:
                    q.append(p)
        flashed = set()
        while q:
            p = q.popleft()
            if p in flashed:
                continue
            flashed.add(p)
            self.total_flashes += 1
            for n in self.get_adjacent(p):
                value = self.bump(n)
                if value > 9:
                    q.append(n)

        for p in flashed:
            self.set_value(p, 0)
        return len(flashed)

    def run(self, count: int):
        for _ in range(count):
            self.do_step()

    def run_until_sync(self):
        total = self.height * self.width
        steps = 0
        count = 0
        while count != total:
            count = self.do_step()
            steps += 1
        return steps


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        grid.run(100)
        result1 = grid.total_flashes

    with timing("Part 2"):
        steps = grid.run_until_sync()
        result2 = 100 + steps

    return (result1, result2)
