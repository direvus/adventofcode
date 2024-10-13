"""Advent of Code 2019

Day 18: Many-Worlds Interpretation

https://adventofcode.com/2019/day/18
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import INF, PriorityQueue, timing


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Grid:
    def __init__(self, stream):
        self.spaces = set()
        self.position = (0, 0)
        self.keys = {}
        self.doors = {}
        self.graph = Graph()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        if isinstance(stream, str):
            stream = stream.split('\n')
        for line in stream:
            line = line.strip()
            if not line:
                continue
            for x, ch in enumerate(line):
                p = (x, y)
                if ch != '#':
                    self.spaces.add(p)

                if ch == '@':
                    self.position = p
                elif ch in string.ascii_lowercase:
                    self.keys[ch] = p
                elif ch in string.ascii_uppercase:
                    self.doors[ch.lower()] = p
            y += 1
        self.make_graph()

    def get_adjacent(self, position: tuple) -> set:
        return {move(position, d) for d in range(len(DIRECTIONS))}

    def make_graph(self):
        """Assemble a graph of the grid space.

        Each square that is an intersection, door, or key will become a node in
        the graph, and linear paths between nodes will become edges.
        """
        graph = Graph()
        pos = self.position
        graph.nodes.add(pos)
        explored = set()
        q = [(pos, 0, pos)]
        doors = set(self.doors.values())
        keys = set(self.keys.values())
        while q:
            pos, cost, start = q.pop(0)
            adjacent = self.get_adjacent(pos) & self.spaces - explored
            if len(adjacent) > 1 or pos in doors or pos in keys:
                graph.nodes.add(pos)
                if cost > 0:
                    graph.edges[start][pos] = cost
                    graph.edges[pos][start] = cost
                cost = 0
                start = pos
            for adj in adjacent:
                q.append((adj, cost + 1, start))
            explored.add(pos)
        self.graph = graph

    def get_neighbours(self, position: tuple, keys: set) -> dict:
        neighbours = self.graph.edges[position]
        locked = {v for k, v in self.doors.items() if k not in keys}
        return {k: v for k, v in neighbours.items() if k not in locked}

    def find_all_keys_path(self) -> int:
        """Return the fewest steps in which we can gather all keys."""
        q = PriorityQueue()
        q.push((frozenset(), self.position), 0)
        target = len(self.keys)
        keynodes = {v: k for k, v in self.keys.items()}
        dist = defaultdict(lambda: INF)
        best = INF
        while q:
            cost, node = q.pop()
            if cost >= best:
                continue
            keys, pos = node
            if len(keys) == target:
                if cost < best:
                    best = cost
                    continue

            neighbours = self.get_neighbours(pos, keys)
            for n, d in neighbours.items():
                newkeys = set(keys)
                if n in keynodes:
                    newkeys.add(keynodes[n])

                newnode = (frozenset(newkeys), n)
                newcost = cost + d
                if newcost < dist[newnode]:
                    dist[newnode] = newcost
                    q.set_priority(newnode, newcost)
        return best


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        grid.make_graph()
        result1 = grid.find_all_keys_path()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
