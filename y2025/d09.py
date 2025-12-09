"""Advent of Code 2025

Day 9: Movie Theatre

https://adventofcode.com/2025/day/9
"""
import logging  # noqa: F401
from itertools import combinations
from operator import add

import grid
from util import get_euclidean_distance, timing


def get_area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def move(a, v):
    return tuple(map(add, a, v))


def line_intersects_y(line, y):
    y1, y2 = sorted((line[0][1], line[1][1]))
    return y1 <= y and y2 >= y


class Grid(grid.SparseGrid):
    def parse(self, stream):
        self.cells = set()
        self.corners = []
        self.interior = {}
        self.verticals = []
        for line in stream:
            x, y = map(int, line.split(','))
            self.cells.add((x, y))
            self.corners.append((x, y))

    def find_largest_rect(self):
        self.areas = [
                (a, b, get_area(a, b))
                for a, b in combinations(self.cells, 2)]
        self.areas.sort(key=lambda x: x[2], reverse=True)
        return self.areas[0][2]

    def contains(self, point):
        if point in self.cells or point in self.green:
            return True

        if point in self.interior:
            return self.interior[point]

        x, y = point
        # Get all the vertical lines that intersect with the point's Y-value.
        verts = [l for l in self.verticals if line_intersects_y(l, y)]

        # The list of verticals is already in sorted X order, so we can step
        # through until we find a line with X value greater than the point's,
        # that will be the nearest vertical right of the point, and the line
        # immediately previous in the list will be the nearest vertical to the
        # left. If the line to the left has a northward direction and the line
        # to the right has a southward direction, the point is contained in the
        # shape. Otherwise, it isn't.
        for i, line in enumerate(verts):
            a, b = line
            if a[0] > x:
                if i == 0:
                    result = False
                else:
                    prev = verts[i - 1]
                    result = (a[1] < b[1] and prev[0][1] > prev[1][1])
                self.interior[point] = result
                return result
        self.interior[point] = False
        return False


    def contains_rect(self, a, b):
        # Trace around the outside of the rectangle. Since this shape consists
        # of a single linear ring, if every point along the boundary is within
        # the polygon, then the entire rectangle is too.
        minx, maxx = sorted((a[0], b[0]))
        miny, maxy = sorted((a[1], b[1]))

        x = minx
        y = miny
        while x <= maxx:
            if not self.contains((x, y)):
                return False
            x += 1
        x -= 1
        y += 1
        while y <= maxy:
            if not self.contains((x, y)):
                return False
            y += 1
        y -= 1
        x -= 1
        while x >= minx:
            if not self.contains((x, y)):
                return False
            x -= 1
        x += 1
        y -= 1
        while y <= miny:
            if not self.contains((x, y)):
                return False
            y -= 1
        return True

    def find_largest_rect_2(self):
        """Find the area of the largest rectangle for Part 2
        """
        # First we have to trace the outline of the shape from the original
        # cells list
        self.green = set()
        length = len(self.cells)
        pos = self.corners[0]
        self.verticals = []
        for i in range(1, length + 1):
            dest = self.corners[i % length]
            if pos[0] == dest[0]:
                v = (0, 1 if dest[1] > pos[1] else -1)
                self.verticals.append((pos, dest))
            elif pos[1] == dest[1]:
                v = (1 if dest[0] > pos[0] else -1, 0)
            else:
                raise Exception(f"Line {pos} -> {dest} is neither vertical nor horizontal!")

            pos = move(pos, v)
            while pos != dest:
                self.green.add(pos)
                pos = move(pos, v)

        self.verticals.sort(key=lambda l: l[0][0])

        # Reuse the area calculation from Part 1, and process the candidate
        # rectangles in largest first order.
        print(f"{len(self.areas)} rectangles to check")
        for a, b, area in self.areas:
            print(f"{a} -> {b}: {area}")
            if self.contains_rect(a, b):
                return area


def parse(stream) -> str:
    grid = Grid()
    grid.parse(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_largest_rect()

    with timing("Part 2"):
        result2 = grid.find_largest_rect_2()

    return (result1, result2)
