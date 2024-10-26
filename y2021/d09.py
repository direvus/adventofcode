"""Advent of Code 2021

Day 9: Smoke Basin

https://adventofcode.com/2021/day/9
"""
import logging  # noqa: F401
from math import prod

from util import timing


class Grid:
    def __init__(self, stream=''):
        self.height = 0
        self.width = 0
        self.heights = []
        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            row = []
            for x, ch in enumerate(line):
                row.append(int(ch))
            self.heights.append(row)
        self.height = len(self.heights)
        self.width = x + 1

    def get_adjacent(self, position: tuple) -> set:
        result = set()
        x, y = position
        if x > 0:
            result.add((x - 1, y))
        if y > 0:
            result.add((x, y - 1))
        if x < self.width - 1:
            result.add((x + 1, y))
        if y < self.height - 1:
            result.add((x, y + 1))
        return result

    def get_value(self, position: tuple):
        x, y = position
        return self.heights[y][x]

    def get_low_points(self) -> set:
        result = set()
        for y in range(self.height):
            for x in range(self.width):
                h = self.get_value((x, y))
                low = True
                for adj in self.get_adjacent((x, y)):
                    if self.get_value(adj) <= h:
                        low = False
                        break
                if low:
                    result.add((x, y))
        return result

    def get_flow_target(self, position: tuple) -> tuple:
        """A cell's flow target is its lowest neighbour."""
        adj = list(self.get_adjacent(position))
        adj.sort(key=lambda x: self.get_value(x))
        return adj[0]

    def get_flows(self, lows) -> dict:
        """Find the flow target for each cell.

        Every cell (except height 9 cells and low points) will have one other
        cell that it flows into. This function returns a mapping of cell
        coordinates to their flow targets.
        """
        result = {}
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                h = self.get_value(p)
                if h > 8 or p in lows:
                    continue
                result[p] = self.get_flow_target(p)
        return result


def parse(stream) -> Grid:
    return Grid(stream)


def get_basins(lows, flows):
    """Get the basins from a set of low points and flow maps."""
    result = {k: {k} for k in lows}
    basins = {k: k for k in lows}
    for cell, target in flows.items():
        if cell in basins:
            # We've already solved this one in passing
            continue
        stack = [cell]
        while target not in basins:
            stack.append(target)
            target = flows[target]
        basin = basins[target]
        for p in stack:
            basins[p] = basin
            result[basin].add(p)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        lows = grid.get_low_points()
        result1 = sum(grid.get_value(p) + 1 for p in lows)

    with timing("Part 2"):
        flows = grid.get_flows(lows)
        basins = get_basins(lows, flows)
        sizes = [len(v) for v in basins.values()]
        sizes.sort(reverse=True)
        result2 = prod(sizes[:3])

    return (result1, result2)
