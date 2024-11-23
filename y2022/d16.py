"""Advent of Code 2022

Day 16: Proboscidea Volcanium

https://adventofcode.com/2022/day/16
"""
import logging  # noqa: F401
import re
from collections import defaultdict

from util import timing, NINF, PriorityQueue


PATTERN = re.compile(
        r'^Valve (\w+) has flow rate=(\d+); .+ valves? (.+)$')


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PATTERN.fullmatch(line)
            name, flow, tunnels = m.groups()
            self.nodes[name] = int(flow)
            self.edges[name] = set(tunnels.split(', '))

    def find_best_release(self, limit: int = 30):
        """Find the best amount of pressure that can be released.

        Given `limit` units of time, find the path through the graph (possibly
        opening the valve at each node) that will ultimately release the most
        pressure.

        Once a valve is open, it releases pressure equal to its flow rate every
        time unit until the limit is reached.

        Moving from one node to an adjacent node costs one time unit, and
        opening a valve also costs one time unit.
        """
        start = ('AA', 0, frozenset())
        q = PriorityQueue()
        q.push(start, 0)
        released = defaultdict(lambda: NINF)
        released[start] = 0
        best = 0
        size = len(self.nodes)

        while q:
            priority, node = q.pop()
            valve, time, opened = node
            pressure = released[node]

            if pressure > best:
                best = pressure

            if time == limit or len(opened) == size:
                # If we've run out of time, or all the valves are opened, then
                # there are no further moves to be made.
                continue

            flow = self.nodes[valve]
            newtime = time + 1
            if flow > 0 and valve not in opened:
                # We could open the valve
                newopen = frozenset(opened | {valve})
                release = flow * (limit - (time + 1)) + pressure
                new = (valve, newtime, newopen)
                if release > released[new]:
                    released[new] = release
                    q.set_priority(new, (-release, newtime))

            for edge in self.edges[valve]:
                # We could move to another valve
                new = (edge, newtime, opened)
                if pressure > released[new]:
                    released[new] = pressure
                q.set_priority(new, (-pressure, newtime))
        return best


def parse(stream) -> Graph:
    graph = Graph()
    graph.parse(stream)
    return graph


def run(stream, test: bool = False):
    with timing("Part 1"):
        graph = parse(stream)
        result1 = graph.find_best_release()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
