#!/usr/bin/env python
from collections import defaultdict
from itertools import pairwise

from rich import print

from util import timing


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.neighbours = defaultdict(set)

    @property
    def order(self):
        return len(self.nodes)

    @property
    def size(self):
        return len(self.edges)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            node, links = line.split(': ')
            links = set(links.split())
            self.nodes.add(node)
            self.nodes |= links
            for link in links:
                edge = frozenset({node, link})
                self.edges.add(edge)
                self.neighbours[node].add(link)
                self.neighbours[link].add(node)

    def to_dot(self) -> str:
        """Return the graph in DOT notation.

        This is useful for exporting to GraphViz.
        """
        lines = ['graph G {']
        for edge in self.edges:
            a, b = tuple(edge)
            lines.append(f'{a} -- {b}')
        lines.append('}')
        return '\n'.join(lines)

    def find_path(self, start: str, end: str, blocked=None) -> list | None:
        """Find a path from node `start` to `end` through the graph.

        This uses a breadth-first search (BFS).  The path will avoid any of the
        edges in the `blocked` set, and will return either a list of edges
        along the path, or else None if no path is found.
        """
        assert start != end
        if blocked is None:
            blocked = set()
        q = [[start]]
        explored = {start}
        while q:
            path = q.pop(0)
            node = path[-1]
            for neighbour in self.neighbours[node]:
                edge = frozenset({node, neighbour})
                if edge in blocked:
                    continue
                if neighbour == end:
                    path.append(end)
                    edges = [frozenset({a, b}) for a, b in pairwise(path)]
                    return edges
                if neighbour in explored:
                    continue
                explored.add(neighbour)
                q.append(path + [neighbour])
        return None

    def get_edge_distinct_paths(self, a: str, b: str) -> list:
        """Return all edge-distinct paths between two nodes.

        The return value is a list of paths, where each path is a list of
        edges.

        If there are no valid paths, return an empty list.
        """
        assert a != b
        blocked = set()
        result = []
        while True:
            path = self.find_path(a, b, blocked)
            if path is None:
                return result
            blocked |= set(path)
            result.append(path)
        return result

    def get_cut_set(self, n: int) -> set:
        """Return the set of `n` edges that disconnect the graph when cut.

        For a given value of `n`, we want to find the `n` pairs of adjacent
        nodes that each have an edge-connectivity value `λ` equal to `n`.

        Each edge is structured as a frozenset of two nodes.
        """
        result = set()
        for a, b in self.edges:
            λ = len(self.get_edge_distinct_paths(a, b))
            if λ == n:
                result.add(frozenset({a, b}))
                if len(result) == n:
                    return result
        raise ValueError("Insufficient cuts found!")

    def cut(self, cuts: set) -> 'Graph':
        """Return a new graph that results from cutting the given edges."""
        g = Graph()
        g.nodes = self.nodes
        g.edges = self.edges - cuts
        for a, b in g.edges:
            g.neighbours[a].add(b)
            g.neighbours[b].add(a)
        return g

    def get_connected_nodes(self, start: str) -> set:
        """Return the set of all nodes that are reachable from `start`.

        The result includes `start` itself.
        """
        q = [start]
        explored = {start}
        while q:
            node = q.pop(0)
            for neighbour in self.neighbours[node]:
                if neighbour in explored:
                    continue
                explored.add(neighbour)
                q.append(neighbour)
        return explored

    def get_subgraphs(self) -> set:
        """Get each of the disconnected subgraphs in this graph.

        Return a set of subgraphs, where each subgraph is a frozenset of node
        names.
        """
        result = set()
        nodes = set(self.nodes)
        while nodes:
            # Choose an arbitrary starting node
            start = tuple(nodes)[0]
            conn = frozenset(self.get_connected_nodes(start))
            result.add(conn)
            nodes -= conn
        return result


def run(stream, test=False):
    with timing("Part 1\n"):
        g = Graph()
        g.parse(stream)
        cuts = g.get_cut_set(3)
        g2 = g.cut(cuts)
        subs = tuple(g2.get_subgraphs())
        assert len(subs) == 2
        result1 = len(subs[0]) * len(subs[1])
    print(f"Result for Part 1 = {result1} \n")

    # There is no Part 2 for Day 25
    return (result1, None)
