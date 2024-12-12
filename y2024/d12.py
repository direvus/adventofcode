"""Advent of Code 2024

Day 12: Garden Groups

https://adventofcode.com/2024/day/12
"""
import logging  # noqa: F401
from collections import deque

from grid import Grid
from util import timing


def get_region(grid, position):
    value = grid.get_value(position)
    q = deque()
    q.append(position)
    result = set()
    perimeter = set()

    while q:
        p = q.popleft()
        if p in result:
            continue
        result.add(p)

        adjacent = grid.get_adjacent(p)
        neighbours = {x for x in adjacent if grid.get_value(x) == value}

        x, y = p
        if (x, y - 1) not in neighbours:
            perimeter.add((1, 1, x, y))
        if (x - 1, y) not in neighbours:
            perimeter.add((0, 1, x, y))
        if (x, y + 1) not in neighbours:
            perimeter.add((1, 0, x, y + 1))
        if (x + 1, y) not in neighbours:
            perimeter.add((0, 0, x + 1, y))
        for n in neighbours:
            q.append(n)
    return result, perimeter


def get_regions(grid):
    visited = set()
    result = []
    for y in range(grid.height):
        for x in range(grid.width):
            p = (x, y)
            if p in visited:
                continue
            region, perimeter = get_region(grid, p)
            value = grid.get_value(p)
            result.append((value, region, perimeter))
            visited.update(region)
    return result


def get_fence_price(region, perimeter):
    return len(region) * len(perimeter)


def count_sides(perimeter):
    result = 0
    visited = set()

    xs = {x for _, _, x, _ in perimeter}
    ys = {y for _, _, _, y in perimeter}

    miny, maxy = min(ys), max(ys)
    minx, maxx = min(xs), max(xs)

    for segment in perimeter:
        if segment in visited:
            continue
        h, f, x, y = segment
        result += 1
        if h:
            # East
            for i in range(x + 1, maxx + 1):
                s = (h, f, i, y)
                if s in perimeter:
                    visited.add(s)
                else:
                    break
            # West
            for i in reversed(range(minx, x)):
                s = (h, f, i, y)
                if s in perimeter:
                    visited.add(s)
                else:
                    break
        else:
            # South
            for i in range(y + 1, maxy + 1):
                s = (h, f, x, i)
                if s in perimeter:
                    visited.add(s)
                else:
                    break
            # North
            for i in reversed(range(miny, y)):
                s = (h, f, x, i)
                if s in perimeter:
                    visited.add(s)
                else:
                    break
    return result


def get_fence_price2(region, perimeter):
    return len(region) * count_sides(perimeter)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        regions = get_regions(grid)
        result1 = sum(get_fence_price(r, p) for _, r, p in regions)

    with timing("Part 2"):
        result2 = sum(get_fence_price2(r, p) for _, r, p in regions)

    return (result1, result2)
