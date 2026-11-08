#!/usr/bin/env python
from itertools import combinations


def get_distance(
        a: tuple,
        b: tuple,
        empty_rows: set,
        empty_cols: set,
        expansion: int,
        ) -> int:
    lowx, highx = sorted([a[1], b[1]])
    lowy, highy = sorted([a[0], b[0]])

    cols = len({x for x in empty_cols if x > lowx and x < highx})
    rows = len({y for y in empty_rows if y > lowy and y < highy})

    return highx - lowx + highy - lowy + ((cols + rows) * (expansion - 1))


def run(stream, test=False):
    height = 0
    width = None
    empty_rows = set()
    empty_cols = set()
    galaxies = []
    for line in stream:
        line = line.strip()
        if width is None:
            width = len(line)
            empty_cols = set(range(width))
        found = False
        for i, c in enumerate(line):
            if c == '#':
                found = True
                galaxies.append((height, i))
                empty_cols.discard(i)
        if not found:
            empty_rows.add(height)
        height += 1

    pairs = list(combinations(galaxies, 2))
    total1 = 0
    total2 = 0
    for a, b in pairs:
        total1 += get_distance(a, b, empty_rows, empty_cols, 2)
        total2 += get_distance(a, b, empty_rows, empty_cols, 10 ** 6)
    return (total1, total2)
