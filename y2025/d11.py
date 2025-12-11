"""Advent of Code 2025

Day 11: Reactor

https://adventofcode.com/2025/day/11
"""
import logging  # noqa: F401
from collections import defaultdict, deque
from io import StringIO

from util import timing


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            a, b = line.split(': ')
            src = a
            dests = set(b.split())
            self.nodes.add(src)
            for dest in dests:
                self.nodes.add(dest)
            self.edges[src] = dests

    def count_paths(self, start, end):
        result = 0
        q = deque()
        q.append(start)

        while q:
            node = q.pop()
            if node == end:
                result += 1
                continue

            for n in self.edges[node]:
                q.append(n)
        return result


def parse(stream) -> str:
    g = Graph()
    g.parse(stream)
    return g


def run(stream, test: bool = False):
    with timing("Part 1"):
        g = parse(stream)
        result1 = g.count_paths('you', 'out')

    if test:
        stream = StringIO("""svr: aaa bbb
                aaa: fft
                fft: ccc
                bbb: tty
                tty: ccc
                ccc: ddd eee
                ddd: hub
                hub: fff
                eee: dac
                dac: fff
                fff: ggg hhh
                ggg: out
                hhh: out""")
        g = parse(stream)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
