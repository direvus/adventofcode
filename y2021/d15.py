"""Advent of Code 2021

Day 15: Chiton

https://adventofcode.com/2021/day/15
"""
import logging  # noqa: F401
from collections import defaultdict

from util import get_manhattan_distance, timing, INF, PriorityQueue


class Grid:
    def __init__(self, stream=''):
        self.height = 0
        self.width = 0
        self.rows = []

        if stream:
            self.parse(stream)

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

    def get_value(self, position: tuple) -> int:
        return self.rows[position[1]][position[0]]

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            row = tuple(int(c) for c in line)
            self.rows.append(row)
        self.height = len(self.rows)
        self.width = len(self.rows[0])

    def find_path(self) -> int:
        """Find the lowest-cost path from the top-left to bottom-right.

        Each cell's value in the grid is the cost to enter that cell.

        Return the total cost of the cheapest path.
        """
        start = (0, 0)
        goal = (self.width - 1, self.height - 1)

        # AStar
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            est, node = q.pop()
            if node == goal:
                return est

            for n in self.get_adjacent(node):
                score = dist[node] + self.get_value(n)
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
        raise ValueError("Did not find any path!")


class MultiGrid(Grid):
    """A grid where values map back to a sub-grid."""
    def get_value(self, position: tuple) -> int:
        x, y = position
        if x < self.subwidth and y < self.subheight:
            return self.rows[y][x]

        xd, xr = divmod(x, self.subwidth)
        yd, yr = divmod(y, self.subheight)

        value = self.rows[yr][xr] - 1  # offset to zero-based for modulo 9
        value = (value + yd + xd) % 9
        return value + 1  # reverse the offset to get values 1-9


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_path()

    with timing("Part 2"):
        mg = MultiGrid()
        mg.rows = grid.rows
        mg.subwidth = grid.width
        mg.subheight = grid.height
        mg.width = grid.width * 5
        mg.height = grid.height * 5
        result2 = mg.find_path()

    return (result1, result2)
