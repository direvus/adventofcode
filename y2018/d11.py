"""Advent of Code 2018

Day 11: Chronal Charge

https://adventofcode.com/2018/day/11
"""
import logging  # noqa: F401

from util import timing, NINF


class Grid:
    def __init__(self, serial: int, size: int = 300):
        self.size = size
        self.serial = serial
        levels = []
        sums = []
        for y in range(self.size):
            row = []
            sumrow = []
            for x in range(self.size):
                power = self.get_power_level((x, y))
                row.append(power)
                total = power
                if x > 0:
                    total += sumrow[-1]
                if y > 0:
                    total += sums[-1][x]
                    if x > 0:
                        total -= sums[-1][x - 1]
                sumrow.append(total)
            levels.append(tuple(row))
            sums.append(tuple(sumrow))
        self.levels = tuple(levels)
        self.sums = tuple(sums)

    def get_power_level(self, cell: tuple) -> int:
        x, y = cell
        rack = x + 10
        power = (rack * y + self.serial) * rack
        hundreds = (power // 100) % 10
        return hundreds - 5

    def get_square_power(self, topleft: tuple, size: int) -> int:
        x, y = topleft
        if size == 1:
            return self.levels[y][x]
        x0, y0 = x - 1, y - 1
        x1, y1 = x + size - 1, y + size - 1
        result = self.sums[y1][x1]
        if x > 0:
            result -= self.sums[y1][x0]
        if y > 0:
            result -= self.sums[y0][x1]
            if x > 0:
                result += self.sums[y0][x0]
        return result

    def get_highest_square(self, size: int = 3) -> tuple:
        best = NINF
        result = None
        for y in range(self.size - size + 1):
            for x in range(self.size - size + 1):
                power = self.get_square_power((x, y), size)
                if power > best:
                    best = power
                    result = (x, y, power)
        return result

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
