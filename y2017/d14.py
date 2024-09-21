"""Advent of Code 2017

Day 14: Disk Defragmentation

https://adventofcode.com/2017/day/14
"""
import logging  # noqa: F401

from y2017.d10 import get_hash
from util import timing


class Grid:
    def __init__(self, key: str, size: int = 128):
        self.size = size
        self.rows = []

        for i in range(size):
            h = get_hash(f'{key}-{i}')
            n = int(h, 16)  # Hash as an integer value
            b = f'{n:0128b}'  # As a bit string
            row = tuple(int(x) for x in b)  # Finally, as a tuple of 0|1 ints
            self.rows.append(row)

    def get_total_used(self) -> int:
        return sum(sum(row) for row in self.rows)

    def get_region(self, node) -> set:
        """Return all the used cells that are connected to the given cell.

        Only horizontal and vertical adjacency is counted, diagonals are not
        considered adjacent.
        """
        q = [node]
        result = set()

        while q:
            y, x = q.pop(0)
            result.add((y, x))
            neighbours = []
            if x > 0:
                neighbours.append((y, x - 1))
            if y > 0:
                neighbours.append((y - 1, x))
            if x < self.size - 1:
                neighbours.append((y, x + 1))
            if y < self.size - 1:
                neighbours.append((y + 1, x))
            for ny, nx in neighbours:
                if (ny, nx) not in result and self.rows[ny][nx]:
                    q.append((ny, nx))
        return result

    def get_num_regions(self) -> int:
        """A region is a contiguous block of adjacent used squares.

        """
        regions = 0
        visited = set()
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                if cell == 0 or (y, x) in visited:
                    continue
                visited |= self.get_region((y, x))
                regions += 1
        return regions


def run(stream, test: bool = False):
    with timing("Part 1"):
        key = stream.readline().strip()
        g = Grid(key)
        result1 = g.get_total_used()

    with timing("Part 2"):
        result2 = g.get_num_regions()

    return (result1, result2)
