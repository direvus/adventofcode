"""Advent of Code 2020

Day 10: Adapter Array

https://adventofcode.com/2020/day/10
"""
import logging  # noqa: F401
from collections import defaultdict, Counter

from util import timing


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        line = line.strip()
        value = int(line)
        result.append(value)
    return result


def find_differences(adapters: list[int]) -> dict:
    diffs = []
    adapters.sort()
    value = 0
    for adapter in adapters:
        diff = adapter - value
        diffs.append(diff)
        value = adapter
    diffs.append(3)
    return Counter(diffs)


class Graph:
    def __init__(self, adapters: list[int]):
        self.nodes = set(adapters)
        self.nodes.add(0)
        self.destinations = defaultdict(set)
        self.solos = []

        for n in sorted(self.nodes):
            self.nodes.add(n)
            adj = {n + x for x in range(1, 4)} & self.nodes
            self.destinations[n] = adj
            if adj == {n + 3}:
                self.solos.append(n)

    def count_paths(self, start: int, end: int) -> int:
        """Return the number of paths between two nodes.

        This will search the paths exhaustively, so it should only be used on
        small regions of the graph.
        """
        q = [(start,)]
        result = 0
        while q:
            path = q.pop(0)
            node = path[-1]
            if node == end:
                result += 1

            for edge in self.destinations[node]:
                if edge <= end:
                    q.append(path + (edge,))
        return result

    def count_full_paths(self) -> int:
        """Return the number of paths from the start to end of the graph.

        The start is always zero, the end is the highest-numbered node.
        Technically the end is actually the highest-numbered node plus 3, but
        since that can't affect the number of paths, we ignore it.
        """
        # Because all paths must flow through all of the solo nodes, we get the
        # answer by searching out the paths between each pair of consecutive
        # solo nodes, and multiplying those all together.
        result = 1
        self.solos.sort()
        node = 0
        end = max(self.nodes)
        for solo in self.solos:
            paths = self.count_paths(node, solo)
            logging.debug(f"{paths} paths from {node} -> {solo}")
            result *= paths
            node = solo
        result *= self.count_paths(node, end)
        return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        adapters = parse(stream)
        diffs = find_differences(adapters)
        result1 = diffs[1] * diffs[3]

    with timing("Part 2"):
        g = Graph(adapters)
        result2 = g.count_full_paths()

    return (result1, result2)
