"""Advent of Code 2019

Day 13: Care Package

https://adventofcode.com/2019/day/13
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing
from y2019.intcode import Computer


class Game:
    def __init__(self):
        self.tiles = defaultdict(lambda: 0)
        self.computer = Computer()

    def run(self):
        while not self.computer.halt:
            try:
                x = next(self.computer.generate())
                y = next(self.computer.generate())
                v = next(self.computer.generate())
                self.tiles[(x, y)] = v
            except StopIteration:
                pass

    def count_tiles(self, value: int) -> int:
        return len(tuple(v for v in self.tiles.values() if v == value))


def parse(stream) -> Game:
    game = Game()
    game.computer.parse(stream.readline().strip())
    return game


def run(stream, test: bool = False):
    if test:
        # No real way to test this, the puzzle did not provide an example
        # input.
        result1, result2 = 0, 0

    with timing("Part 1"):
        game = parse(stream)
        game.run()
        result1 = game.count_tiles(2)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
