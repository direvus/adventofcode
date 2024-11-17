"""Advent of Code 2022

Day 8: Treetop Tree House

https://adventofcode.com/2022/day/8
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            self.rows.append(tuple(int(x) for x in line))
            y += 1
        self.height = y
        self.width = len(line)

    def is_visible_up(self, x: int, y: int, value: int) -> bool:
        for dy in range(y):
            if self.rows[dy][x] >= value:
                return False
        return True

    def is_visible_down(self, x: int, y: int, value: int) -> bool:
        for dy in range(y + 1, self.height):
            if self.rows[dy][x] >= value:
                return False
        return True

    def is_visible_left(self, x: int, y: int, value: int) -> bool:
        for dx in range(x):
            if self.rows[y][dx] >= value:
                return False
        return True

    def is_visible_right(self, x: int, y: int, value: int) -> bool:
        for dx in range(x + 1, self.width):
            if self.rows[y][dx] >= value:
                return False
        return True

    def is_visible(self, position: tuple) -> bool:
        x, y = position
        if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
            # On the edge of the grid, so it is always visible.
            return True
        value = self.rows[y][x]
        return (
                self.is_visible_up(x, y, value) or
                self.is_visible_down(x, y, value) or
                self.is_visible_left(x, y, value) or
                self.is_visible_right(x, y, value))

    def count_visible(self) -> int:
        result = 0
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                visible = self.is_visible(p)
                if visible:
                    result += 1
        return result

    def get_score(self, position: tuple) -> int:
        result = 1
        x, y = position
        value = self.rows[y][x]

        for dy in range(y - 1, -1, -1):
            if self.rows[dy][x] >= value:
                break
        result *= y - dy

        for dy in range(y + 1, self.height):
            if self.rows[dy][x] >= value:
                break
        result *= dy - y

        for dx in range(x - 1, -1, -1):
            if self.rows[y][dx] >= value:
                break
        result *= x - dx

        for dx in range(x + 1, self.width):
            if self.rows[y][dx] >= value:
                break
        result *= dx - x
        return result

    def get_highest_score(self) -> int:
        result = 0
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                p = (x, y)
                score = self.get_score(p)
                if score > result:
                    result = score
        return result


def parse(stream) -> Grid:
    grid = Grid()
    grid.parse(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.count_visible()

    with timing("Part 2"):
        result2 = grid.get_highest_score()

    return (result1, result2)
