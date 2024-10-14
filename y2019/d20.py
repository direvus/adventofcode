"""Advent of Code 2019

Day 20: Donut Maze

https://adventofcode.com/2019/day/20
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import INF, PriorityQueue, timing


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)

    def simplify(self, keep: set = None):
        """Simplify this graph by removing redundant nodes

        We remove all nodes that only connect between two other nodes,
        replacing them with a single edge. Continue until no such nodes remain.

        Any nodes mentioned in `keep` will not be removed regardless.
        """
        if keep is None:
            keep = set()
        removable = [
                (k, v) for k, v in self.edges.items()
                if len(v) == 2 and k not in keep]
        while removable:
            for node, edges in removable:
                self.nodes.discard(node)
                self.edges.pop(node, None)
                others = tuple(edges.keys())
                cost = sum(edges.values())
                for other in others:
                    self.edges[other].pop(node, None)
                a, b = others
                self.edges[a][b] = cost
                self.edges[b][a] = cost
            removable = [
                    (k, v) for k, v in self.edges.items()
                    if len(v) == 2 and k not in keep]


class Grid:
    def __init__(self, stream):
        self.spaces = set()
        self.portals = {}
        self.start = (0, 0)
        self.end = (0, 0)
        self.graph = Graph()

        if stream:
            self.parse(stream)
            self.make_graph()

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')

        y = 0
        letters = {}
        for line in stream:
            line.strip('\n')
            x = 0
            for ch in line:
                p = (x, y)
                if ch in string.ascii_uppercase:
                    letters[p] = ch
                elif ch == '.':
                    self.spaces.add(p)
                x += 1
            y += 1
        portals = {}
        for pos, letter in letters.items():
            x, y = pos
            code = None
            if (x, y + 1) in letters:
                code = letter + letters[(x, y + 1)]
                # For vertical markers, the space being labelled can be either
                # above or below the marker.
                if (x, y + 2) in self.spaces:
                    space = (x, y + 2)
                else:
                    space = (x, y - 1)
            elif (x + 1, y) in letters:
                code = letter + letters[(x + 1, y)]
                # For horizontal markers, the space being labelled can be
                # either left or right of the marker.
                if (x + 2, y) in self.spaces:
                    space = (x + 2, y)
                else:
                    space = (x - 1, y)

            if code and space:
                if code == 'AA':
                    self.start = space
                elif code == 'ZZ':
                    self.end = space
                elif code in portals:
                    other = portals[code]
                    self.portals[space] = other
                    self.portals[other] = space
                else:
                    portals[code] = space

    def get_adjacent(self, position: tuple) -> set:
        x, y = position
        return {(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)}

    def get_neighbours(self, position: tuple) -> dict:
        return self.graph.edges[position]

    def make_graph(self):
        """Assemble a graph of the grid space.

        Each square that is an intersection or portal endpoint will become a
        node in the graph, and linear paths between nodes will become edges.
        The connections between portal endpoints become edges with a cost of
        one.
        """
        graph = Graph()
        graph.nodes.add(self.start)
        graph.nodes.add(self.end)
        keep = {self.start, self.end} | set(self.portals.keys())
        explored = set()
        pos = self.start
        q = [(pos, 0, pos)]
        while q:
            pos, cost, start = q.pop(0)
            adjacent = self.get_adjacent(pos) & self.spaces
            if pos in self.portals:
                adjacent.add(self.portals[pos])
            adjacent -= explored
            if len(adjacent) > 1 or pos in keep:
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
        self.graph.simplify(keep)

    def find_path(self) -> int:
        self.dist = defaultdict(lambda: INF)
        self.dist[self.start] = 0
        q = PriorityQueue()
        explored = set()
        q.push(self.start, 0)

        while q:
            cost, node = q.pop()
            if node == self.end:
                return cost
            neighbours = self.get_neighbours(node)
            for n, d in neighbours.items():
                if n in explored:
                    continue
                score = cost + d
                if score < self.dist[n]:
                    self.dist[n] = score
                    q.set_priority(n, score)
            explored.add(node)


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_path()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
