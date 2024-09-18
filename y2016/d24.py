"""Advent of Code 2016

Day 24: Air Duct Spelunking

https://adventofcode.com/2016/day/24
"""
import logging  # noqa: F401
from collections import defaultdict
from itertools import combinations, permutations

from util import timing, get_manhattan_distance, PriorityQueue


INF = float('inf')
TARGETS = '0123456789'


class Grid:
    def __init__(self):
        self.rows = []
        self.targets = {}
        self.start = None
        self.width = None
        self.height = None

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            row = []
            for x, ch in enumerate(line):
                row.append(int(ch != '#'))
                if ch in TARGETS:
                    self.targets[int(ch)] = (y, x)
                    if ch == '0':
                        self.start = (y, x)
            self.rows.append(tuple(row))
            y += 1
        self.rows = tuple(self.rows)
        self.height = y
        self.width = x + 1

    def get_neighbours(self, node) -> set:
        # This puzzle input is fully enclosed by walls, so don't need to check
        # for going out of bounds.
        y, x = node
        points = ((y + 1, x), (y, x + 1), (y - 1, x), (y, x - 1))
        return {(y, x) for y, x in points if self.rows[y][x]}

    def find_shortest_path(self, start, goal) -> int:
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            for n in self.get_neighbours(node):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
        raise ValueError("Ran out of moves to try!")

    def find_target_paths(self) -> dict:
        """For each distinct pair of targets, find the shortest path.

        The return value is a dict, keyed by a set of two points for each pair
        of target nodes, including the start node. The values of the dict are
        the number of steps in the shortest path between those nodes.
        """
        result = {}
        for a, b in combinations(self.targets.keys(), 2):
            a_node = self.targets[a]
            b_node = self.targets[b]
            steps = self.find_shortest_path(a_node, b_node)
            result[frozenset({a, b})] = steps
        return result

    def find_optimal_path(self) -> int:
        """Find the optimal path that visits all targets.

        The path must begin at the start node (target 0) and pass through each
        of the other targets at least once.

        Return the length of the shortest such path.
        """
        best = INF
        paths = self.find_target_paths()
        targets = tuple(k for k in self.targets.keys() if k != 0)
        for perm in permutations(targets, len(targets)):
            start = 0
            length = 0
            for k in perm:
                pair = frozenset({start, k})
                length += paths[pair]
                start = k
            if length < best:
                best = length
        return best


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        result1 = grid.find_optimal_path()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
