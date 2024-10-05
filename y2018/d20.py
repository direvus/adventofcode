"""Advent of Code 2018

Day 20: A Regular Map

https://adventofcode.com/2018/day/20
"""
import logging  # noqa: F401
from collections import defaultdict

from util import get_manhattan_distance, timing, INF, PriorityQueue


MOVES = {
        'N': lambda p: (p[0], p[1] - 1),
        'E': lambda p: (p[0] + 1, p[1]),
        'S': lambda p: (p[0], p[1] + 1),
        'W': lambda p: (p[0] - 1, p[1]),
        }


def move(point: tuple, direction: str) -> tuple:
    return MOVES[direction](point)


class Exp:
    def __init__(self):
        self.nodes = {}
        self.children = defaultdict(set)
        self.root = 0

    def parse(self, stream):
        if isinstance(stream, str):
            line = stream.strip()
        else:
            line = stream.readline().strip()
        # Remove the first and last characters (always ^ and $)
        exp = line[1:-1]
        parent = set()
        group = []
        stack = []
        i = 0
        n = 0
        while i < len(exp):
            chars = []
            while i < len(exp) and exp[i] not in '(|)':
                chars.append(exp[i])
                i += 1

            node = ''.join(chars)
            self.nodes[n] = node
            group.append(n)
            for p in parent:
                self.children[p].add(n)

            if i >= len(exp):
                break

            if exp[i] == '(':
                # Start a new branch group
                parent = {n}
                stack.append(parent)
                group = []
            elif exp[i] == '|':
                # Set parent to the stack tip
                parent = stack[-1]
            elif exp[i] == ')':
                # End this branch group
                parent = set(group)
                stack.pop()
                group = []

            n += 1
            i += 1


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)
        self.dist = defaultdict(lambda: INF)

    def build(self, exp: Exp):
        """Build the graph by walking through an Exp tree."""
        start = (0, 0)
        self.nodes.add(start)
        q = [(start, 0)]
        explored = set()
        while q:
            start, node = q.pop()
            if node in explored:
                continue
            pos = start
            directions = exp.nodes[node]

            for d in directions:
                new = move(pos, d)
                self.nodes.add(new)
                self.edges[pos].add(new)
                self.edges[new].add(pos)
                pos = new

            explored.add(node)
            for child in exp.children[node]:
                q.append((pos, child))

    def parse(self, stream):
        exp = Exp()
        exp.parse(stream)
        logging.debug(f"Expression has {len(exp.nodes)} nodes")
        self.build(exp)
        logging.debug(f"Graph has {len(self.nodes)} nodes")

    def get_neighbours(self, node: tuple) -> set:
        return self.edges[node]

    def find_path(self, start: tuple, goal: tuple) -> int | None:
        """Find the shortest path from `start` to `goal`.

        Return the number of steps in the shortest path, or None if the goal is
        not reachable.

        Best distances from the start point for each node are cached so you can
        quickly find paths from the same start node to different goals. If you
        want to search from a different start point, you must clear the cache
        yourself.
        """
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        self.dist[start] = 0
        explored = set()

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            for n in self.get_neighbours(node):
                score = self.dist[node] + 1
                if score < self.dist[n]:
                    self.dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
            explored.add(node)
        return None

    def find_furthest_path(self, start: tuple = (0, 0)) -> int:
        """Find the distance to the furthest node from `start`.

        The furthest node is the one whose shortest path from `start` is the
        longest overall.
        """
        # Use a Dijkstra to get the shortest distance to each node in the
        # graph, and then return the largest one.
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        q = PriorityQueue()
        explored = set()
        q.push(start, 0)

        while q:
            cost, node = q.pop()
            score = cost + 1
            for n in self.get_neighbours(node):
                if n in explored:
                    continue
                if score < dist[n]:
                    dist[n] = score
                    q.set_priority(n, score)
            explored.add(node)
        return max(x for x in dist.values() if x < INF)


def run(stream, test: bool = False):
    with timing("Part 1"):
        g = Graph()
        g.parse(stream)
        result1 = g.find_furthest_path()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
