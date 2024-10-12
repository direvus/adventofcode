"""Advent of Code 2019

Day 17: Set and Forget

https://adventofcode.com/2019/day/17
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Grid:
    def __init__(self, stream=None):
        self.scaffolds = set()
        self.position = (0, 0)
        self.direction = 0
        self.computer = Computer()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        self.computer.parse(stream)

    def get_neighbours(self, position: tuple) -> set:
        adjacent = {move(position, d) for d in range(len(DIRECTIONS))}
        return adjacent & self.scaffolds

    def get_intersections(self) -> set:
        result = set()
        for p in self.scaffolds:
            if len(self.get_neighbours(p)) > 2:
                result.add(p)
        return result

    def get_total_alignments(self) -> int:
        total = 0
        for p in self.get_intersections():
            total += p[0] * p[1]
        return total

    def run(self) -> str:
        result = []
        y = 0
        x = 0
        for code in self.computer.generate():
            ch = chr(code)
            if ch == '\n':
                y += 1
                x = 0
                result.append(ch)
                continue
            elif ch == '#':
                self.scaffolds.add((x, y))
            elif ch in DIRECTIONS:
                self.direction = DIRECTIONS.index(ch)
                self.position = (x, y)
                self.scaffolds.add((x, y))
            result.append(ch)
            x += 1
        return ''.join(result)


def parse(stream) -> Grid:
    return Grid(stream.readline().strip())


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        grid = parse(stream)
        grid.run()
        result1 = grid.get_total_alignments()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
