"""Advent of Code 2022

Day 12: Hill Climbing Algorithm

https://adventofcode.com/2022/day/12
"""
import logging  # noqa: F401
from collections import defaultdict
from functools import cache

from util import get_manhattan_distance, timing, INF, PriorityQueue


@cache
def get_adjacent(x, y, width, height):
    result = set()
    if x > 0:
        result.add((x - 1, y))
    if y > 0:
        result.add((x, y - 1))
    if x < width - 1:
        result.add((x + 1, y))
    if y < height - 1:
        result.add((x, y + 1))
    return result


class Grid:
    def __init__(self):
        self.rows = []
        self.height = 0
        self.width = 0
        self.start = None
        self.goal = None

    def parse(self, stream):
        y = 0
        base = ord('a')
        for line in stream:
            line = line.strip()
            row = []
            for x, ch in enumerate(line):
                if ch == 'S':
                    self.start = (x, y)
                    row.append(0)
                elif ch == 'E':
                    self.goal = (x, y)
                    row.append(25)
                else:
                    height = ord(ch) - base
                    row.append(height)
            self.rows.append(row)
            y += 1
        self.height = y
        self.width = x + 1

    def get_value(self, position: tuple) -> int:
        return self.rows[position[1]][position[0]]

    def get_adjacent(self, position: tuple) -> set:
        return get_adjacent(*position, self.width, self.height)

    def get_neighbours(self, position: tuple) -> set:
        adj = self.get_adjacent(position)
        limit = self.get_value(position) + 1
        return {x for x in adj if self.get_value(x) <= limit}

    def get_positions_at_height(self, height: int) -> set:
        result = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.get_value((x, y)) == height:
                    result.add((x, y))
        return result

    def find_path(self, start=None) -> int:
        if not start:
            start = self.start
        # AStar
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, self.goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            est, node = q.pop()
            if node == self.goal:
                return est

            for n in self.get_neighbours(node):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, self.goal)
                    q.set_priority(n, f)
        raise ValueError("Did not find any path!")

    def find_best_start_path(self):
        result = INF
        options = self.get_positions_at_height(0) - {self.start}
        for option in options:
            try:
                steps = self.find_path(option)
                if steps < result:
                    result = steps
            except ValueError:
                pass
        return result


def parse(stream) -> Grid:
    g = Grid()
    g.parse(stream)
    return g


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_path()

    with timing("Part 2"):
        result2 = grid.find_best_start_path()

    return (result1, result2)
