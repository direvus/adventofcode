"""Advent of Code 2019

Day 18: Many-Worlds Interpretation

https://adventofcode.com/2019/day/18
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import INF, PriorityQueue, get_manhattan_distance, timing


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Grid:
    def __init__(self, stream):
        self.spaces = set()
        self.position = (0, 0)
        self.keys = {}
        self.doors = {}

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        if isinstance(stream, str):
            stream = stream.split('\n')
        for line in stream:
            line = line.strip()
            if not line:
                continue
            for x, ch in enumerate(line):
                p = (x, y)
                if ch != '#':
                    self.spaces.add(p)

                if ch == '@':
                    self.position = p
                elif ch in string.ascii_lowercase:
                    self.keys[ch] = p
                elif ch in string.ascii_uppercase:
                    self.doors[ch.lower()] = p
            y += 1

    def get_neighbours(self, position: tuple, keys: set) -> set:
        adjacent = {move(position, d) for d in range(len(DIRECTIONS))}
        spaces = adjacent & self.spaces
        locked = {v for k, v in self.doors.items() if k not in keys}
        return spaces - locked

    def find_path(self, start: tuple, goal: tuple, keys: set) -> int | None:
        """Find the shortest path from `start` to `goal`.

        Return the number of steps in the shortest path, or None if the goal is
        not reachable.
        """
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            for n in self.get_neighbours(node, keys):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
        return None

    def find_keys_path(self, keys) -> int | None:
        """Return the number of steps taken to get the keys in this order.

        Return None if the order is not viable.
        """
        steps = 0
        position = self.position
        held = set()
        for k in keys:
            target = self.keys[k]
            path = self.find_path(position, target, held)
            if path is None:
                return None
            steps += path
            held.add(k)
            position = target
        return steps

    def find_all_keys_path(self) -> int:
        """Return the fewest steps in which we can gather all keys."""
        q = PriorityQueue()
        q.push((0, frozenset(), self.position), (0, 0))
        best = INF
        while q:
            _, node = q.pop()
            cost, keys, pos = node
            if cost >= best:
                continue
            logging.debug(f"At {pos} with {keys} after {cost} moves ...")
            targets = set(self.keys.keys()) - keys
            if not targets:
                logging.debug(f"  collected all keys in {cost} moves")
                if cost < best:
                    logging.debug("  >>> NEW BEST PATH!")
                    best = cost
                continue
            for k in targets:
                goal = self.keys[k]
                path = self.find_path(pos, goal, keys)
                if path is None:
                    continue
                logging.debug(f"  could reach {k} in {path} moves")
                newkeys = keys | {k}
                newcost = cost + path
                node = (newcost, frozenset(newkeys), goal)
                priority = (-len(newkeys), newcost)
                q.set_priority(node, priority)
        return best


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        logging.debug(vars(grid))
        result1 = grid.find_all_keys_path()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
