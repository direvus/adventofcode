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

    def contains_hline(self, a, b):
        y = a[1]
        for line in self.vbreaks:
            x = line[0][0]
            if x < a[0]:
                continue
            if x >= b[0]:
                break
            if line[0][1] <= y and line[1][1] >= y:
                return False
        return True

    def contains_vline(self, a, b):
        x = a[0]
        for line in self.hbreaks:
            y = line[0][1]
            if y < a[1]:
                continue
            if y >= b[1]:
                break
            if line[0][0] >= x and line[1][0] <= x:
                return False
        return True

    def contains_point(self, point):
        if point in self.cells:
            return True

        x, y = point
        # Check if the point happens to lie on a horizontal line.
        for l in self.horizontals:
            if l[0][1] != y:
                continue
            x1, x2 = sorted((l[0][0], l[1][0]))
            if x1 <= x and x2 >= x:
                return True

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
            if a[0] == x:
                return True
            if a[0] > x:
                if i == 0:
                    return False
                else:
                    prev = verts[i - 1]
                    return (a[1] < b[1] and prev[0][1] > prev[1][1])
        return False

    def contains_rect(self, a, b):
        # Since this shape consists of a single linear ring, if every line
        # along the boundary is within the polygon, then the entire rectangle
        # is too.
        minx, maxx = sorted((a[0], b[0]))
        miny, maxy = sorted((a[1], b[1]))

        nw = (minx, miny)
        ne = (maxx, miny)
        se = (maxx, maxy)
        sw = (minx, maxy)

        return (
                self.contains_point(nw) and
                self.contains_point(ne) and
                self.contains_point(se) and
                self.contains_point(sw) and
                self.contains_hline(nw, ne) and
                self.contains_vline(ne, se) and
                self.contains_hline(sw, se) and
                self.contains_vline(nw, sw))

    def find_largest_rect_2(self):
        """Find the area of the largest rectangle for Part 2
        """
        # First we have to trace the outline of the shape from the original
        # cells list
        length = len(self.corners)
        pos = self.corners[0]
        self.verticals = []
        self.horizontals = []
        self.vbreaks = []
        self.hbreaks = []
        for i in range(1, length + 1):
            dest = self.corners[i % length]
            if pos[0] == dest[0]:
                v = (0, 1 if dest[1] > pos[1] else -1)
                self.verticals.append((pos, dest))
                if v[1] > 0:
                    self.vbreaks.append((pos, dest))
            elif pos[1] == dest[1]:
                v = (1 if dest[0] > pos[0] else -1, 0)
                self.horizontals.append((pos, dest))
                if v[0] < 0:
                    self.hbreaks.append((pos, dest))
            else:
                raise Exception(f"Line {pos} -> {dest} is neither vertical nor horizontal!")
            pos = dest

        self.verticals.sort(key=lambda l: l[0][0])
        self.horizontals.sort(key=lambda l: l[0][1])
        self.vbreaks.sort(key=lambda l: l[0][0])
        self.hbreaks.sort(key=lambda l: l[0][1])

        # Reuse the area calculation from Part 1, and process the candidate
        # rectangles in largest first order.
        for a, b, area in self.areas:
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
