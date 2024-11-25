"""Advent of Code 2022

Day 16: Proboscidea Volcanium

https://adventofcode.com/2022/day/16
"""
import logging  # noqa: F401
import re
from collections import defaultdict
from itertools import combinations

from util import timing, INF, NINF, PriorityQueue


PATTERN = re.compile(
        r'^Valve (\w+) has flow rate=(\d+); .+ valves? (.+)$')


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)
        self.paths = defaultdict(list)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PATTERN.fullmatch(line)
            name, flow, tunnels = m.groups()
            self.nodes[name] = int(flow)
            self.edges[name] = set(tunnels.split(', '))
        self.find_paths()

    def find_path(self, start: str, end: str):
        """Find the best route between two nodes.

        Return the best path as a list of node names, including the start and
        end nodes.
        """
        if end in self.edges[start]:
            # The nodes are adjacent
            return [start, end]

        # Dijkstra
        q = PriorityQueue()
        q.push(start, 0)
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        explored = set()
        sources = {}

        while q:
            cost, node = q.pop()

            if node == end:
                break

            score = cost + 1
            for n in self.edges[node]:
                if n in explored:
                    continue
                if score < dist[n]:
                    dist[n] = score
                    sources[n] = node
                    q.set_priority(n, score)
            explored.add(node)
        result = [end]
        while node in sources:
            node = sources[node]
            result.append(node)
        result.reverse()
        return result

    def find_paths(self):
        """Find the best route between each pair of openable valves."""
        valves = {n for n in self.nodes if n == 'AA' or self.nodes[n] > 0}
        for a, b in combinations(valves, 2):
            path = self.find_path(a, b)
            for i in range(len(path) - 1):
                self.paths[frozenset({path[i], b})] = path[i:]

    def get_next_node_on_path(self, start, end):
        path = self.paths[frozenset({start, end})]
        if path[0] == start:
            return path[1]
        else:
            return path[-2]

    def find_best_release(self, limit: int = 30):
        """Find the best amount of pressure that can be released.

        Given `limit` units of time, find the path through the graph (possibly
        opening a valve at each node) that will ultimately release the most
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
        targets = {node for node, flow in self.nodes.items() if flow > 0}
        size = len(targets)

        while q:
            priority, node = q.pop()
            valve, time, opened = node
            pressure = released[node]

            if pressure > best:
                best = pressure

            if time >= limit or len(opened) == size:
                # If we've run out of time, or all the valves that can be
                # opened are open, then there are no further moves to be made.
                continue

            # For each remaining openable valve, queue up a move to that valve.
            for target in targets - opened - {valve}:
                path = self.paths[frozenset({valve, target})]
                newtime = time + len(path)
                new = (target, newtime, frozenset(opened | {target}))
                flow = self.nodes[target]
                release = flow * (limit - newtime) + pressure
                if newtime <= limit and release > released[new]:
                    released[new] = release
                    q.set_priority(new, (-release, newtime))
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
