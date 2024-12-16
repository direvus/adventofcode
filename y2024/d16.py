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

        while q:
            est, node = q.pop()
            position, facing = node
            if position == self.end:
                return est

            cost = dist[node]
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

            for n in neighbours:
                node, cost = n
                if cost < dist[node]:
                    dist[node] = cost
                    f = cost + grid.get_distance(node[0], self.end)
                    q.set_priority(node, f)
        return False

    def find_best_path_tiles(self, limit):
        """Find all paths through the maze that cost no more than `limit`.

        Return all of the cells that occur along any of those paths, as a set.
        """
        result = {self.start, self.end}
        q = PriorityQueue()
        node = (self.start, 1)
        q.push(node, grid.get_distance(self.start, self.end))
        dist = defaultdict(lambda: INF)
        dist[node] = 0
        trace = defaultdict(set)
        ends = set()

        while q:
            est, node = q.pop()
            position, facing = node
            if position == self.end:
                ends.add(node)
                continue

            cost = dist[node]
            if cost >= limit:
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
        while q:
            node = q.popleft()
            result.add(node[0])
            q.extend(trace[node])

        return result


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        result1 = grid.find_best_path()

    with timing("Part 2"):
        result2 = len(grid.find_best_path_tiles(result1))

    return (result1, result2)
