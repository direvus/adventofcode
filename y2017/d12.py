"""Advent of Code 2017

Day 12: Digital Plumber

https://adventofcode.com/2017/day/12
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing


class Graph:
    """A bidirectional graph."""
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
            node, links = line.split(' <-> ')
            node = int(node)
            links = {int(x) for x in links.split(', ')}
            self.nodes.add(node)
            self.nodes |= links
            for link in links:
                edge = frozenset({node, link})
                self.edges.add(edge)
                self.neighbours[node].add(link)
                self.neighbours[link].add(node)

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

    def get_group_size(self, node: int) -> int:
        """Get the number of nodes connected to this node."""
        return len(self.get_connected_nodes(node))

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

    def get_num_groups(self) -> int:
        """Return the number of groups (disconnected subgraphs)."""
        return len(self.get_subgraphs())


def run(stream, test: bool = False):
    with timing("Part 1"):
        g = Graph()
        g.parse(stream)
        result1 = g.get_group_size(0)

    with timing("Part 2"):
        result2 = g.get_num_groups()

    return (result1, result2)
