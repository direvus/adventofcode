"""Advent of Code 2021

Day 12: Passage Pathing

https://adventofcode.com/2021/day/12
"""
import logging  # noqa: F401
from collections import defaultdict, deque, Counter

from util import timing


class Graph:
    def __init__(self, stream):
        self.nodes = set()
        self.edges = defaultdict(set)

        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            a, b = line.split('-')
            self.nodes.add(a)
            self.nodes.add(b)
            self.edges[a].add(b)
            self.edges[b].add(a)

    def count_paths(self) -> int:
        q = deque()
        q.append(('start',))
        result = 0
        while q:
            path = q.popleft()
            last = path[-1]
            if last == 'end':
                result += 1
                continue

            # small caves may not be revisited
            visited = {x for x in path if x.islower()}
            neighbours = self.edges[last] - visited

            for n in neighbours:
                q.append(path + (n,))
        return result

    def count_paths2(self) -> int:
        q = deque()
        q.append(('start',))
        result = 0
        while q:
            path = q.popleft()
            last = path[-1]
            if last == 'end':
                result += 1
                continue

            # revisiting 'start' is never allowed
            neighbours = self.edges[last] - {'start'}

            # If any small cave has been visited twice, no other small cave may
            # be revisited.
            visited = tuple(x for x in path if x.islower())
            counts = Counter(visited)
            max_count = counts.most_common(1)[0][1]
            if max_count > 1:
                neighbours -= set(visited)

            for n in neighbours:
                q.append(path + (n,))
        return result


def parse(stream) -> Graph:
    return Graph(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        graph = parse(stream)
        result1 = graph.count_paths()

    with timing("Part 2"):
        result2 = graph.count_paths2()

    return (result1, result2)
