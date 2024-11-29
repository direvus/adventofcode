"""Advent of Code 2022

Day 24: Blizzard Basin

https://adventofcode.com/2022/day/24
"""
import logging  # noqa: F401
from collections import defaultdict
from functools import cache

from util import get_manhattan_distance, timing, INF, PriorityQueue


FACING = ('>', 'v', '<', '^')
VECTORS = ((1, 0), (0, 1), (-1, 0), (0, -1))


@cache
def move(position: tuple, facing: int, count: int = 1) -> tuple:
    x, y = position
    vx, vy = VECTORS[facing]
    return (x + vx * count, y + vy * count)


@cache
def get_distance(a: tuple, b: tuple):
    return get_manhattan_distance(a, b)


class Grid:
    def __init__(self):
        self.start = (0, -1)
        self.end = None
        self.width = 0
        self.height = 0
        self.blizzards = []

    def parse(self, stream):
        # The coordinate system doesn't include the outer walls.
        y = -1
        for line in stream:
            line = line.strip()
            for i, ch in enumerate(line):
                if ch in FACING:
                    x = i - 1
                    blizzard = (x, y, FACING.index(ch))
                    self.blizzards.append(blizzard)
            y += 1
        self.height = y - 1
        self.width = i - 1
        self.end = i - 2, y - 1

    @cache
    def get_blizzard_positions(self, time: int):
        result = []
        for x, y, f in self.blizzards:
            t = time if f < 2 else -time
            if f % 2:
                y = (y + t) % self.height
            else:
                x = (x + t) % self.width
            result.append((x, y))
        return result

    @cache
    def in_bounds(self, position: tuple):
        if position == self.start or position == self.end:
            return True
        x, y = position
        return (
                x >= 0 and y >= 0 and
                x < self.width and y < self.height)

    @cache
    def get_neighbours(self, position: tuple, time: int) -> set:
        adjacent = {move(position, i) for i in range(4)}
        spaces = adjacent | {position}  # Waiting is a valid option too
        blizzards = set(self.get_blizzard_positions(time))
        spaces -= blizzards
        return {p for p in spaces if self.in_bounds(p)}

    def find_path(self, start: tuple, end: tuple, starttime: int = 0) -> int:
        """Find the fastest path from the start to the end, avoiding blizzards.

        Return the time taken on the best path.
        """
        # AStar
        q = PriorityQueue()
        node = start, starttime
        q.push(node, get_distance(start, end))
        dist = defaultdict(lambda: INF)
        dist[node] = 0

        while q:
            est, node = q.pop()
            position, time = node
            if position == end:
                return est

            neighbours = self.get_neighbours(position, time + 1)

            for p in neighbours:
                score = dist[node] + 1
                n = (p, time + 1)
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_distance(p, end)
                    q.set_priority(n, f)
        raise ValueError("Did not find any path!")

    def find_return_path(self, starttime: int) -> int:
        """Find the fastest path end -> start -> end.

        Return the total time taken on the best path.
        """
        result = self.find_path(self.end, self.start, starttime)
        result += self.find_path(self.start, self.end, starttime + result)
        return result


def parse(stream) -> Grid:
    grid = Grid()
    grid.parse(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_path(grid.start, grid.end)

    with timing("Part 2"):
        result2 = result1 + grid.find_return_path(result1)

    return (result1, result2)
