"""Advent of Code 2018

Day 11: Chronal Charge

https://adventofcode.com/2018/day/11
"""
import logging  # noqa: F401

from util import timing, NINF


def get_square_power(levels: tuple, topleft: tuple, size: int) -> int:
    x, y = topleft
    result = 0
    for i in range(y, y + size):
        result += sum(levels[i][x: x + size])
    return result


def get_highest_square(levels: tuple, size: int = 3) -> tuple:
    best = NINF
    result = None
    length = len(levels)
    for y in range(length - size + 1):
        for x in range(length - size + 1):
            power = get_square_power(levels, (x, y), size)
            if power > best:
                best = power
                result = (x, y, power)
    return result


class Grid:
    def __init__(self, serial: int, size: int = 300):
        self.size = size
        self.serial = serial
        levels = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(self.get_power_level((x, y)))
            levels.append(tuple(row))
        self.levels = tuple(levels)

    def get_power_level(self, cell: tuple) -> int:
        x, y = cell
        rack = x + 10
        power = (rack * y + self.serial) * rack
        hundreds = (power // 100) % 10
        return hundreds - 5

    def get_square_power(self, topleft: tuple, size: int) -> int:
        return get_square_power(self.levels, topleft, size)

    def get_highest_square(self, size: int = 3) -> tuple:
        return get_highest_square(self.levels, size)

    def get_highest_any_square(self) -> tuple:
        best = NINF
        result = None
        losing_streak = 0
        for size in range(1, 301):
            x, y, power = self.get_highest_square(size)
            if power > best:
                best = power
                result = (x, y, size)
                losing_streak = 0
            else:
                losing_streak += 1
                if losing_streak > 4:
                    # At this point it's probably just going to keep getting
                    # worse, so stop here.
                    return result
        return result


def parse(stream) -> int:
    return int(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        serial = parse(stream)
        grid = Grid(serial)
        x, y, power = grid.get_highest_square(3)
        result1 = (x, y)

    with timing("Part 2"):
        result2 = grid.get_highest_any_square()

    return (result1, result2)
