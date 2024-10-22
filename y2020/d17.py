"""Advent of Code 2020

Day 17: Conway Cubes

https://adventofcode.com/2020/day/17
"""
import logging  # noqa: F401
from collections import defaultdict
from itertools import product

from util import timing


class Grid3:
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


class Grid4:
    """An infinite four-dimensional grid for a Conway's Game of Life."""
    def __init__(self, stream=None):
        self.active = set()
        self.extents = defaultdict(lambda: [0, 0])
        if stream:
            self.parse(stream)

    def get_adjacents(self, position: tuple) -> set[tuple]:
        x, y, z, w = position
        return {
                (x + dx, y + dy, z + dz, w + dw)
                for dz in range(-1, 2)
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                for dw in range(-1, 2)} - {position}

    def count_adjacent_active(self, position: tuple) -> int:
        return len(self.get_adjacents(position) & self.active)

    def update_extents(self, extents: dict, position: tuple):
        result = {}
        for i, coord in enumerate(position):
            low, high = extents[i]
            result[i] = [min(low, coord), max(high, coord)]
        return result

    def update(self):
        newactive = set()
        newextents = dict(self.extents)
        ranges = [range(a - 1, b + 2) for a, b in self.extents.values()]
        for p in product(*ranges):
            count = self.count_adjacent_active(p)
            active = p in self.active
            if count == 3 or (count == 2 and active):
                newactive.add(p)
                newextents = self.update_extents(newextents, p)
        self.active = newactive
        self.extents = newextents

    def run(self, count: int = 1):
        for i in range(count):
            self.update()


def parse(stream) -> Grid3:
    return Grid3(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        active = frozenset(grid.active)

        grid.run(6)
        result1 = len(grid.active)

    with timing("Part 2"):
        grid = Grid4()
        # Add the initial set of active nodes from the 3D grid, with the fourth
        # dimension set to all zero, and keep the extents updated.
        for p3 in active:
            p4 = p3 + (0,)
            grid.active.add(p4)
            grid.extents = grid.update_extents(grid.extents, p4)

        grid.run(6)
        result2 = len(grid.active)

    return (result1, result2)
