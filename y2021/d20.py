"""Advent of Code 2021

Day 20: Trench Map

https://adventofcode.com/2021/day/20
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self, stream=''):
        self.pixels = set()
        self.pattern = ''
        self.outers = False
        self.miny = 0
        self.maxy = 0
        self.minx = 0
        self.maxx = 0

        if stream:
            self.parse(stream)

    def parse(self, stream):
        line = stream.readline().strip()
        self.pattern = tuple(x == '#' for x in line)
        # Consume one blank line
        stream.readline()

        y = 0
        for line in stream:
            for x, ch in enumerate(line.strip()):
                if ch == '#':
                    self.pixels.add((x, y))
            y += 1
        self.maxy = y - 1
        self.maxx = x

    def get_pixel(self, position) -> bool:
        x, y = position
        if (
                x >= self.minx and x <= self.maxx and
                y >= self.miny and y <= self.maxy):
            return position in self.pixels
        else:
            return self.outers

    def get_scan_window(self, position: tuple):
        x, y = position
        return (
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                )

    def get_enhancement_value(self, position) -> int:
        result = 0
        scan = self.get_scan_window(position)
        for i, p in enumerate(reversed(scan)):
            if self.get_pixel(p):
                result += 1 << i
        return result

    def get_next_pixel(self, position) -> bool:
        index = self.get_enhancement_value(position)
        return self.pattern[index]

    def update(self):
        pixels = set()
        for y in range(self.miny - 1, self.maxy + 2):
            for x in range(self.minx - 1, self.maxx + 2):
                p = (x, y)
                if self.get_next_pixel(p):
                    pixels.add(p)
        self.pixels = pixels
        self.minx -= 1
        self.maxx += 1
        self.miny -= 1
        self.maxy += 1
        if self.pattern[0]:
            self.outers = not self.outers

    def do_updates(self, count: int):
        for _ in range(count):
            self.update()


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        logging.debug(vars(grid))
        grid.update()
        grid.update()
        result1 = len(grid.pixels)

    with timing("Part 2"):
        grid.do_updates(48)
        result2 = len(grid.pixels)

    return (result1, result2)
