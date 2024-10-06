"""Advent of Code 2018

Day 22: Mode Maze

https://adventofcode.com/2018/day/22
"""
import logging  # noqa: F401
from collections import defaultdict

from util import get_manhattan_distance, timing, INF, PriorityQueue


TYPES = '.=|'
TOOLS = ('none', 'torch', 'climb')


def get_adjacent(position: tuple) -> set[tuple]:
    x, y = position
    result = {(x, y + 1), (x + 1, y)}
    if x > 0:
        result.add((x - 1, y))
    if y > 0:
        result.add((x, y - 1))
    return result


def trace_to_path(trace: dict, end: tuple) -> list:
    result = [end]
    node = end
    while node in trace:
        result.insert(0, trace[node])
        node = trace[node]
    return result


class Grid:
    def __init__(self, depth: int, target: tuple):
        self.depth = depth
        self.target = target
        self.levels = {}

    def get_index(self, location: tuple) -> int:
        if location == (0, 0) or location == self.target:
            return 0
        x, y = location
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return self.get_level((x - 1, y)) * self.get_level((x, y - 1))

    def get_level(self, location: tuple) -> int:
        if location in self.levels:
            return self.levels[location]
        index = self.get_index(location)
        level = (index + self.depth) % 20183
        self.levels[location] = level
        return level

    def get_type(self, location: tuple) -> int:
        return self.get_level(location) % 3

    def get_risk(self) -> int:
        total = 0
        for x in range(self.target[0] + 1):
            for y in range(self.target[1] + 1):
                total += self.get_type((x, y))
        return total

    def get_neighbours(self, node: tuple) -> dict:
        """Return possible moves from this node.

        Nodes are tuples of (x, y, tool) integers, and we return the neighbours
        as a dict of node => cost.
        """
        x, y, tool = node
        result = {}
        currtype = self.get_type((x, y))
        for loc in get_adjacent((x, y)):
            nexttype = self.get_type(loc)
            if tool != nexttype:
                # Current tool is suitable, can move there in one
                # time unit.
                result[loc + (tool,)] = 1
        # Can always stay where we are and change tools for seven time units.
        for i in range(len(TOOLS)):
            if i not in {tool, currtype}:
                result[(x, y, i)] = 7
        return result

    def estimate_distance(self, node: tuple) -> int:
        """Estimate the distance from this node to the target.

        This is intended as a cost heuristic for A Star pathfinding. It uses
        the manhattan distance, plus a fixed cost of seven to change tools, if
        the current tool is not the torch.
        """
        tool = 0 if node[2] == 1 else 7
        return get_manhattan_distance(node[:2], self.target) + tool

    def find_path(self) -> int:
        """Find the fastest path from (0, 0) to the target.

        The torch must be equipped at both the start and the target.

        Return the total time taken in the shortest path.
        """
        q = PriorityQueue()
        start = (0, 0, 1)
        goal = self.target + (1,)
        q.push(start, sum(self.target))
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        trace = {}

        while q:
            cost, node = q.pop()
            logging.debug(f"At {node} with cost {dist[node]} ...")
            if node == goal:
                logging.debug(trace_to_path(trace, goal))
                return cost

            neighbours = self.get_neighbours(node)
            for n, cost in neighbours.items():
                score = dist[node] + cost
                if score < dist[n]:
                    dist[n] = score
                    trace[n] = node
                    f = score + self.estimate_distance(n)
                    q.set_priority(n, f)
        return None


def parse(stream) -> Grid:
    line = stream.readline().strip()
    depth = int(line.split()[-1])

    line = stream.readline().strip()
    target = tuple(int(x) for x in line.split()[-1].split(','))
    return Grid(depth, target)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.get_risk()

    with timing("Part 2"):
        result2 = grid.find_path()

    return (result1, result2)
