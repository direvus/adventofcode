"""Advent of Code 2020

Day 17: Conway Cubes

https://adventofcode.com/2020/day/17
"""
import logging  # noqa: F401

from util import timing


class Grid:
    """An infinite cubic grid for a Conway's Game of Life."""
    def __init__(self, stream=None):
        self.active = set()
        self.extent = [0, 0, 0, 0, 0, 0]
        if stream:
            self.parse(stream)

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        z = 0
        y = 0
        for line in stream:
            line = line.strip()
            if line == '':
                continue
            for x, ch in enumerate(line):
                if ch == '#':
                    self.active.add((x, y, z))
            y += 1
        self.extent[3] = y - 1
        self.extent[1] = x - 1

    def get_adjacents(self, position: tuple) -> set[tuple]:
        x, y, z = position
        return {
                (x + dx, y + dy, z + dz)
                for dz in range(-1, 2)
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                if dz != 0 or dy != 0 or dx != 0}

    def count_adjacent_active(self, position: tuple) -> int:
        return len(self.get_adjacents(position) & self.active)

    def update(self):
        newactive = set()
        newextent = [0, 0, 0, 0, 0, 0]
        for z in range(self.extent[4] - 1, self.extent[5] + 2):
            for y in range(self.extent[2] - 1, self.extent[3] + 2):
                for x in range(self.extent[0] - 1, self.extent[1] + 2):
                    p = (x, y, z)
                    count = self.count_adjacent_active(p)
                    active = p in self.active
                    if count == 3 or (count == 2 and active):
                        newactive.add(p)
                        newextent = [
                                min(newextent[0], x), max(newextent[1], x),
                                min(newextent[2], y), max(newextent[3], y),
                                min(newextent[4], z), max(newextent[5], z),
                                ]
        self.active = newactive
        self.extent = newextent

    def run(self, count: int = 1):
        for i in range(count):
            self.update()

    def zslice_to_str(self, z: int = 0):
        lines = []
        for y in range(self.extent[2], self.extent[3] + 1):
            line = []
            for x in range(self.extent[2], self.extent[3] + 1):
                line.append('#' if (x, y, z) in self.active else '.')
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        grid.run(6)
        result1 = len(grid.active)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
