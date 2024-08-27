#!/usr/bin/env python
import sys

from util import timing, move, Direction, Point


class Grid:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.rocks = set()
        self.start = None

    def is_valid(self, point):
        return (
                point.y >= 0 and point.y < self.height and
                point.x >= 0 and point.x < self.width and
                point not in self.rocks)


def parse_grid(stream) -> Grid:
    grid = Grid()
    y = 0
    for line in stream:
        line = line.strip()
        grid.width = len(line)
        for x, char in enumerate(line):
            if char == '#':
                grid.rocks.add(Point(y, x))
            elif char == 'S':
                grid.start = Point(y, x)
        y += 1
    grid.height = y
    return grid


def run(grid: Grid, count: int) -> set[Point]:
    points = set([grid.start])
    for i in range(count):
        new = set()
        for p in points:
            for d in Direction:
                candidate = move(p, d)
                if grid.is_valid(candidate):
                    new.add(candidate)
        points = new
    return points


if __name__ == '__main__':
    grid = parse_grid(sys.stdin)

    # Part 1
    with timing("Part 1\n"):
        points = run(grid, 64)
        result = len(points)
    print(f"Result for Part 1 = {result} \n")

    # Part 2
