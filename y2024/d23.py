"""Advent of Code 2024

Day 23: LAN Party

https://adventofcode.com/2024/day/23
"""
import logging  # noqa: F401
from collections import defaultdict, deque
from itertools import combinations

from util import timing


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_edge(self, a, b):
        self.nodes.add(a)
        self.nodes.add(b)
        self.edges[a].add(b)
        self.edges[b].add(a)

    def find_triples(self, prefix='t'):
        result = set()
        for node in self.nodes:
            if not node.startswith(prefix):
                continue
            for a, b in combinations(self.edges[node], 2):
                if b in self.edges[a]:
                    result.add(frozenset((node, a, b)))
        return result

    def fully_connected(self, nodes):
        for a, b in combinations(nodes, 2):
            if b not in self.edges[a]:
                return False
        return True

    def find_groups(self, size):
        result = set()
        for node in self.nodes:
            for group in combinations(self.edges[node], size - 1):
                if self.fully_connected(group):
                    result.add(frozenset(group + (node,)))
        return result

    def find_largest_group(self):
        n = 4
        prev = None
        groups = None
        while groups is None or len(groups):
            prev = groups
            groups = self.find_groups(n)
            n += 1
        # We expect there will be exactly one group with the largest size.
        assert len(prev) == 1
        return next(iter(prev))


def parse(stream) -> str:
    return tuple(line.strip().split('-') for line in stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        graph = Graph()
        for edge in parsed:
            graph.add_edge(*edge)
        triples = graph.find_triples('t')
        result1 = len(triples)

    with timing("Part 2"):
        group = graph.find_largest_group()
        nodes = sorted(list(group))
        result2 = ','.join(nodes)

    return (result1, result2)
