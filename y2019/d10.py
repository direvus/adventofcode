"""Advent of Code 2019

Day 10: Monitoring Station

https://adventofcode.com/2019/day/10
"""
import logging  # noqa: F401
from math import gcd, atan2

from util import NINF, TWOπ, get_manhattan_distance, timing


def move(point: tuple, vector: tuple) -> tuple:
    return tuple(x + vector[i] for i, x in enumerate(point))


def get_angle(origin: tuple, point: tuple) -> float:
    vector = tuple(x - origin[i] for i, x in enumerate(point))
    return atan2(vector[0], -vector[1]) % TWOπ


class Grid:
    def __init__(self):
        self.nodes = set()
        self.height = 0
        self.width = 0

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        y = 0
        for line in stream:
            line = line.strip()
            for x, ch in enumerate(line):
                if ch == '#':
                    self.nodes.add((x, y))
            y += 1
        self.height = y + 1
        self.width = x + 1

    def get_occlusions(self, point: tuple) -> set:
        """Return the positions that are occluded from a point of view.

        Considering each other node in the field, find the smallest integer
        vector from the point of view to that node, and mark all the positions
        'behind' that node as occluded.

        We can save some cycles by prioritising nodes that are closer to the
        point of view, and ignoring any nodes that have already been marked as
        occluded.

        Return the set of positions that are occluded.
        """
        result = set()
        nodes = list(self.nodes - {point})
        nodes.sort(key=lambda x: get_manhattan_distance(point, x))
        for node in nodes:
            if node in result:
                # This node is already hidden
                continue
            vector = (node[0] - point[0], node[1] - point[1])
            div = gcd(*vector)
            vector = tuple(x // div for x in vector)

            x, y = move(node, vector)
            while x >= 0 and x < self.width and y >= 0 and y < self.height:
                result.add((x, y))
                x, y = move((x, y), vector)
        return result

    def find_best_viewpoint(self) -> tuple:
        """Find the node with line-of-sight to the most other nodes.

        Considering each node, count the number of other nodes that are not
        occluded from that point of view. Return the point of view with the
        highest such count, along with the count itself, as a tuple.
        """
        best = NINF
        result = None
        for node in self.nodes:
            occ = self.get_occlusions(node)
            count = len(self.nodes - occ - {node})
            if count > best:
                best = count
                result = node
        return result, best

    def fire_ze_laser(self, point: tuple, limit: int) -> tuple:
        """Fire a rotating laser until we destroy `limit` asteroids.

        The laser starts pointing north, rotates clockwise, and destroys the
        first asteroid it hits on each trajectory.

        We continue firing until we have destroyed `limit` asteroids, then we
        stop and return the coordinates of the last asteroid destroyed.
        """
        count = 0
        nodes = self.nodes - {point}
        while count < limit:
            # Calculate the occlusions, based on the nodes we've removed so
            # far.
            occ = self.get_occlusions(point)
            targets = list(nodes - occ)

            # These are all the targets we could hit on the current sweep. Sort
            # them in order of angle from the Y axis, then destroy each one in
            # that order, removing it from the grid.
            targets.sort(key=lambda x: get_angle(point, x))
            for target in targets:
                self.nodes -= {target}
                count += 1
                if count == limit:
                    break
        return target


def parse(stream) -> Grid:
    g = Grid()
    g.parse(stream)
    return g


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        node, count = grid.find_best_viewpoint()
        result1 = count

    with timing("Part 2"):
        coords = grid.fire_ze_laser(node, 200)
        result2 = coords[0] * 100 + coords[1]

    return (result1, result2)
