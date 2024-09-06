#!/usr/bin/env python
from array import array
from functools import cache
from itertools import chain

from util import timing, Point


class Grid:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.rocks = set()
        self.start = None


@cache
def is_valid(height, width, point) -> bool:
    return (
            point.y >= 0 and point.y < height and
            point.x >= 0 and point.x < width)


@cache
def normalise(height, width, point) -> Point:
    return Point(point.y % height, point.x % width)


def get_neighbours(p: Point) -> Point:
    return (
            Point(p.y - 1, p.x),
            Point(p.y + 1, p.x),
            Point(p.y, p.x - 1),
            Point(p.y, p.x + 1),
            )


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


def walk_grid(grid: Grid, count: int) -> set[Point]:
    points = set([grid.start])
    for i in range(count):
        new = set()
        for p in points:
            for n in get_neighbours(p):
                if is_valid(grid.height, grid.width, n):
                    new.add(n)
        points = new - grid.rocks
    return points


def grid_to_array(grid: Grid) -> array:
    values = []
    for y in range(grid.height):
        for x in range(grid.width):
            v = 0 if Point(y, x) in grid.rocks else 1
            values.append(v)
    return array('B', values)


def get_array_value(height, width, arr, point) -> bool:
    i = ((point.y % height) * width) + (point.x % width)
    return arr[i]


def walk_grid2(grid: Grid, count: int) -> set[Point]:
    points = set([grid.start])
    arr = grid_to_array(grid)

    def filt(x):
        return get_array_value(grid.height, grid.width, arr, x)

    for i in range(count):
        n = chain.from_iterable(map(get_neighbours, points))
        points = set(filter(filt, n))
    return points


def get_square_points(points, height, width, y, x):
    """Filter for points that lie in the given map square.

    Map squares are numbered starting from 0, 0 for the original map. y
    increases downwards and x increases leftwards.
    """
    top = y * height
    bottom = (y + 1) * height
    left = x * width
    right = (x + 1) * width
    return filter(lambda x: (
            x.y >= top and x.y < bottom and
            x.x >= left and x.x < right), points)


def run(stream, test=False):
    grid = parse_grid(stream)

    # Part 1
    with timing("Part 1\n"):
        points = walk_grid(grid, 6)
        result1 = len(points)
    print(f"Result for Part 1 = {result1} \n")

    # Part 2
    with timing("Part 2\n"):
        count = (131 * 2) + 65
        h = grid.height
        w = grid.width
        with timing(f"Executing {count} steps"):
            points = walk_grid2(grid, count)
            total = len(points)
        print(f"Got {total} total points")

        full_odd = len(set(get_square_points(points, h, w, 0, 0)))
        print(f"Got {full_odd} full odd points on home square")
        full_even = len(set(get_square_points(points, h, w, 1, 0)))
        print(f"Got {full_even} full even points on y+1 square")
        major_odd_se = len(set(get_square_points(points, h, w, 1, 1)))
        major_odd_ne = len(set(get_square_points(points, h, w, -1, 1)))
        major_odd_sw = len(set(get_square_points(points, h, w, 1, -1)))
        major_odd_nw = len(set(get_square_points(points, h, w, -1, -1)))
        print(f"Got {major_odd_ne} major odd points on y+1, x+1 square")
        print(f"Got {major_odd_se} major odd points on y-1, x+1 square")
        print(f"Got {major_odd_nw} major odd points on y+1, x-1 square")
        print(f"Got {major_odd_sw} major odd points on y-1, x-1 square")
        minor_even_se = len(set(get_square_points(points, h, w, 2, 1)))
        minor_even_ne = len(set(get_square_points(points, h, w, -2, 1)))
        minor_even_sw = len(set(get_square_points(points, h, w, 2, -1)))
        minor_even_nw = len(set(get_square_points(points, h, w, -2, -1)))
        print(f"Got {minor_even_se} minor even points on y+2, x+1 square")
        print(f"Got {minor_even_ne} minor even points on y-2, x+1 square")
        print(f"Got {minor_even_sw} minor even points on y+2, x-1 square")
        print(f"Got {minor_even_nw} minor even points on y-2, x-1 square")

        n = 26501365 // 131
        result2 = sum([
                full_odd * ((n - 1) ** 2),
                full_even * (n ** 2),
                major_odd_se * (n - 1),
                major_odd_ne * (n - 1),
                major_odd_sw * (n - 1),
                major_odd_nw * (n - 1),
                minor_even_se * n,
                minor_even_ne * n,
                minor_even_sw * n,
                minor_even_nw * n,
                len(set(get_square_points(points, h, w, 2, 0))),
                len(set(get_square_points(points, h, w, -2, 0))),
                len(set(get_square_points(points, h, w, 0, 2))),
                len(set(get_square_points(points, h, w, 0, -2))),
                ])
    print(f"Result for Part 2 = {result2} \n")
    return (result1, result2)
