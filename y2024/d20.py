"""Advent of Code 2024

Day 20: Race Condition

https://adventofcode.com/2024/day/20
"""
import logging  # noqa: F401
from collections import defaultdict, deque, Counter
from functools import cache

import grid
from util import timing, INF, PriorityQueue


def parse(stream) -> str:
    return stream.readline().strip()


class Grid(grid.SparseGrid):
    def __init__(self):
        super().__init__()
        self.walls = set()
        self.start = None
        self.end = None

    def parse_cell(self, position, value):
        if value == '#':
            self.walls.add(position)
        elif value == 'S':
            self.start = position
        elif value == 'E':
            self.end = position

    @cache
    def get_neighbours(self, position):
        return set(self.get_adjacent(position)) - self.walls

    def find_best_path(self):
        q = PriorityQueue()
        node = self.start
        q.push(node, grid.get_distance(self.start, self.end))
        dist = defaultdict(lambda: INF)
        dist[node] = 0
        trace = {}

        while q:
            est, position = q.pop()
            if position == self.end:
                path = [position]
                while position in trace:
                    path.append(trace[position])
                    position = trace[position]
                return tuple(reversed(path))

            neighbours = self.get_neighbours(position)
            for n in neighbours:
                cost = dist[position] + 1
                if cost < dist[n]:
                    dist[n] = cost
                    f = cost + grid.get_distance(n, self.end)
                    q.set_priority(n, f)
                    trace[n] = position
        return None

    def find_cheats(self, path):
        result = []
        for i, position in enumerate(path):
            for j in range(i + 3, len(path)):
                target = path[j]
                if grid.get_distance(position, target) == 2:
                    result.append((position, target, j - i - 2))
        return result

    def find_cheats_limit(self, path, limit: int = 20):
        result = []
        for i, position in enumerate(path):
            for j in range(i + 3, len(path)):
                target = path[j]
                steps = j - i
                dist = grid.get_distance(position, target)
                if dist <= limit and dist < steps:
                    result.append((position, target, steps - dist))
        return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        path = grid.find_best_path()
        cheats = grid.find_cheats(path)
        minimum = 50 if test else 100
        result1 = sum(int(x[2] >= minimum) for x in cheats)

    with timing("Part 2"):
        cheats = grid.find_cheats_limit(path, 20)
        savings = tuple(x[2] for x in cheats if x[2] >= minimum)
        counts = Counter(savings)
        result2 = counts.total()

    return (result1, result2)
