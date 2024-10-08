"""Advent of Code 2019

Day 6: Universal Orbit Map

https://adventofcode.com/2019/day/6
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing


class Tree:
    def __init__(self):
        self.nodes = set()
        self.children = defaultdict(set)
        self.parent = {}

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            parent, child = line.split(')')
            self.nodes.add(parent)
            self.nodes.add(child)
            self.children[parent].add(child)
            self.parent[child] = parent

    def add_node(self, node: str, parent: str):
        self.nodes.add(node)
        self.children[parent].add(node)
        self.parent[node] = parent

    def count_ancestors(self, node: str) -> int:
        """Count the number of ancestors of a node."""
        result = 0
        while node in self.parent:
            node = self.parent[node]
            result += 1
        return result

    def count_orbits(self) -> int:
        """Count the total number of orbits in this tree.

        This is the sum of the number of ancestors of every node.
        """
        result = 0
        for node in self.nodes:
            result += self.count_ancestors(node)
        return result

    def find_path(self, a: str, b: str) -> int:
        """Find the length of the shortest path between two nodes."""
        if a == b:
            return 0

        # We walk up the tree from both nodes until we find their closest
        # common ancestor, then the length of the shortest path is just the
        # sum of the lengths between each node and the common ancestor.
        parents = [a]
        node = a
        count = 0
        while node in self.parent:
            node = self.parent[node]
            count += 1
            if node == b:
                return count
            parents.append(node)

        node = b
        count = 0
        while node in self.parent:
            node = self.parent[node]
            count += 1
            if node in parents:
                count += parents.index(node)
                return count
        raise ValueError("No path found")

    def count_transfers(self, a: str, b: str) -> int:
        return self.find_path(self.parent[a], self.parent[b])


def parse(stream) -> Tree:
    t = Tree()
    t.parse(stream)
    return t


def run(stream, test: bool = False):
    with timing("Part 1"):
        tree = parse(stream)
        result1 = tree.count_orbits()

    with timing("Part 2"):
        if test:
            tree.add_node('YOU', 'K')
            tree.add_node('SAN', 'I')
        result2 = tree.count_transfers('YOU', 'SAN')

    return (result1, result2)
