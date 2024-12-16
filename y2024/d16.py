"""Advent of Code 2024

Day 16: Reindeer Maze

https://adventofcode.com/2024/day/16
"""
import logging  # noqa: F401
from collections import defaultdict, deque

import grid
from util import timing, INF, PriorityQueue


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

    def find_best_path(self):
        q = PriorityQueue()
        facing = 1  # East
        node = (self.start, facing)
        q.push(node, grid.get_distance(self.start, self.end))
        dist = defaultdict(lambda: INF)
        dist[node] = 0
        trace = defaultdict(set)
        ends = set()
        best = None

        while q:
            est, node = q.pop()
            position, facing = node
            if position == self.end:
                ends.add(node)
                best = dist[node]
                continue

            cost = dist[node]
            if best is not None and cost >= best:
                continue

            neighbours = set()
            left = grid.turn(facing, -1)
            right = grid.turn(facing, 1)

            if grid.move(position, left, 1) not in self.walls:
                neighbours.add(((position, left), cost + 1000))
            if grid.move(position, right, 1) not in self.walls:
                neighbours.add(((position, right), cost + 1000))

            ahead = grid.move(position, facing, 1)
            if ahead not in self.walls:
                neighbours.add(((ahead, facing), cost + 1))

            origin = node
            for n in neighbours:
                node, cost = n
                if cost < dist[node]:
                    dist[node] = cost
                    f = cost + grid.get_distance(node[0], self.end)
                    q.set_priority(node, f)
                    trace[node].add(origin)
                elif cost == dist[node]:
                    # An equally good option for reaching this node
                    trace[node].add(origin)

        q = deque()
        q.extend(ends)
        tiles = set()
        while q:
            node = q.popleft()
            tiles.add(node[0])
            q.extend(trace[node])

        return best, tiles


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        result1, tiles = grid.find_best_path()

    with timing("Part 2"):
        result2 = len(tiles)

    return (result1, result2)
