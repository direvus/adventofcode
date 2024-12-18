"""Advent of Code 2024

Day 18: RAM Run

https://adventofcode.com/2024/day/18
"""
import logging  # noqa: F401
from collections import defaultdict
from functools import cache

import grid
from util import timing, INF, PriorityQueue


class Grid(grid.SparseGrid):
    def __init__(self, size):
        self.width = size
        self.height = size
        self.blocks = []

    @cache
    def get_neighbours(self, position, time):
        adjacent = self.get_adjacent(position)
        corrupt = self.blocks[:time]
        return {x for x in adjacent if x not in corrupt}

    def find_best_path(self, time):
        q = PriorityQueue()
        start = (0, 0)
        end = (self.width - 1, self.height - 1)
        q.push(start, grid.get_distance(start, end))
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        trace = {}

        while q:
            est, p = q.pop()
            if p == end:
                path = [p]
                while p in trace:
                    path.append(trace[p])
                    p = trace[p]
                return tuple(reversed(path))

            neighbours = self.get_neighbours(p, time)
            for n in neighbours:
                cost = dist[p] + 1
                if cost < dist[n]:
                    dist[n] = cost
                    f = cost + grid.get_distance(n, end)
                    q.set_priority(n, f)
                    trace[n] = p

    def find_last_viable_time(self, path, mintime):
        for t in range(mintime + 1, len(self.blocks)):
            if self.blocks[t - 1] not in path:
                # The path is still intact so don't re-calculate it.
                continue
            path = self.find_best_path(t)
            if path is None:
                return t - 1


def parse(stream) -> str:
    return tuple(tuple(map(int, line.strip().split(','))) for line in stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        size = 7 if test else 71
        time = 12 if test else 1024
        grid = Grid(size)
        grid.blocks = parsed
        path = grid.find_best_path(time)
        result1 = len(path) - 1

    with timing("Part 2"):
        index = grid.find_last_viable_time(path, time)
        result2 = ','.join(map(str, grid.blocks[index]))

    return (result1, result2)
