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
        """Simplify this graph by removing uninteresting nodes.

        For all nodes that are not listed in `keep`, and have fewer than three
        connections, we remove the node. If the node had two connections, we
        replace it with an edge joining the two other nodes. If the node had
        one or zero connections, we remove it entirely.
        """
        if keep is None:
            keep = set()
        removable = [
                (k, v) for k, v in self.edges.items()
                if len(v) < 3 and k not in keep]
        while removable:
            for node, edges in removable:
                self.nodes.discard(node)
                self.edges.pop(node, None)
                others = tuple(edges.keys())
                cost = sum(edges.values())
                for other in others:
                    self.edges[other].pop(node, None)
                if len(others) == 2:
                    a, b = others
                    self.edges[a][b] = cost
                    self.edges[b][a] = cost
            removable = [
                    (k, v) for k, v in self.edges.items()
                    if len(v) < 3 and k not in keep]


class Grid:
    def __init__(self, stream):
        self.spaces = set()
        self.portals = {}
        self.markers = {}
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
                self.markers[space] = code
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
        """Assemble a graph of the grid space."""
        graph = Graph()
        keep = {self.start, self.end} | set(self.portals.keys())
        explored = set()
        pos = self.start
        q = [pos]
        while q:
            pos = q.pop(0)
            adjacent = self.get_adjacent(pos) & self.spaces
            if pos in self.portals:
                adjacent.add(self.portals[pos])
            graph.nodes.add(pos)
            for adj in adjacent:
                graph.edges[pos][adj] = 1
                graph.edges[adj][pos] = 1
                if adj not in explored:
                    q.append(adj)
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


class LevelGrid(Grid):
    def __init__(self, grid: Grid):
        self.spaces = frozenset(grid.spaces)
        self.portals = dict(grid.portals)
        self.markers = dict(grid.markers)
        self.start = grid.start
        self.end = grid.end
        self.graph = grid.graph

        xs = {p[0] for p in self.spaces}
        ys = {p[1] for p in self.spaces}
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)

    def on_outer_edge(self, position: tuple):
        return (
                position[0] in {self.minx, self.maxx} or
                position[1] in {self.miny, self.maxy})

    def find_path(self) -> int | None:
        logging.debug(sorted(self.graph.nodes, key=lambda x: (x[1], x[0])))
        logging.debug(self.graph.edges)
        self.dist = defaultdict(lambda: INF)
        self.dist[(self.start, 0)] = 0
        goal = (self.end, 0)
        q = PriorityQueue()
        explored = set()
        q.push((self.start, 0), 0)

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost
            pos, level = node
            neighbours = self.get_neighbours(pos)
            for p, d in neighbours.items():
                newlevel = level
                if pos in self.portals and p == self.portals[pos]:
                    newlevel += -1 if self.on_outer_edge(pos) else 1
                newnode = (p, newlevel)
                if newnode in explored or newlevel < 0:
                    continue
                score = cost + d
                if score < self.dist[newnode]:
                    self.dist[newnode] = score
                    q.set_priority(newnode, score)
            explored.add(node)


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_path()

    with timing("Part 2"):
        lg = LevelGrid(grid)
        result2 = lg.find_path()

    return (result1, result2)
