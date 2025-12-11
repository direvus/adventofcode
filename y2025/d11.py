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
        self.paths = {}

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
        # Memoized DFS
        if (start, end) in self.paths:
            return self.paths[(start, end)]

        if start == end:
            return 1

        count = sum(self.count_paths(n, end) for n in self.edges[start])
        self.paths[(start, end)] = count
        return count


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
        with timing("svr -> fft"):
            a = g.count_paths('svr', 'fft')
        with timing("fft -> dac"):
            b = g.count_paths('fft', 'dac')
        with timing("dac -> out"):
            c = g.count_paths('dac', 'out')

        result2 = a * b * c

    return (result1, result2)
