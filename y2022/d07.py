"""Advent of Code 2022

Day 7: No Space Left On Device

https://adventofcode.com/2022/day/7
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing, INF


TOTAL_SIZE = 70000000
REQUIRED_SPACE = 30000000


class Tree:
    def __init__(self):
        self.nodes = [['/', 0]]
        self.children = defaultdict(dict)
        self.parent = {}

    def add_node(self, parent: int, name: str, size: int = 0) -> int:
        self.nodes.append([name, size])
        nodeid = len(self.nodes) - 1
        self.children[parent][name] = nodeid
        self.parent[nodeid] = parent
        if size > 0:
            d = nodeid
            while d in self.parent:
                d = self.parent[d]
                self.nodes[d][1] += size
        return nodeid

    def get_total_size(self, limit: int):
        result = 0
        for i, (name, size) in enumerate(self.nodes):
            if size <= limit and i in self.children:
                result += size
        return result

    def get_smallest_dir(self, limit: int):
        result = INF
        for i, (name, size) in enumerate(self.nodes):
            if size >= limit and size < result and i in self.children:
                result = size
        return result


def parse(stream) -> Tree:
    tree = Tree()
    cwd = 0
    for line in stream:
        line = line.strip()
        match line.split():
            case ['$', 'cd', '/']:
                cwd = 0
            case ['$', 'cd', '..']:
                cwd = tree.parent[cwd]
            case ['$', 'cd', name]:
                cwd = tree.children[cwd][name]
            case ['$', 'ls']:
                pass
            case ['dir', name]:
                tree.add_node(cwd, name, 0)
            case [size, name]:
                tree.add_node(cwd, name, int(size))
    return tree


def run(stream, test: bool = False):
    with timing("Part 1"):
        tree = parse(stream)
        result1 = tree.get_total_size(100000)

    with timing("Part 2"):
        req = REQUIRED_SPACE - TOTAL_SIZE + tree.nodes[0][1]
        result2 = tree.get_smallest_dir(req)

    return (result1, result2)
