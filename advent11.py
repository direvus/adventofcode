#!/usr/bin/env python
import sys
from itertools import combinations


def get_distance(a: tuple, b: tuple) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


if __name__ == '__main__':
    height = 0
    width = None
    empty_cols = set()
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if width is None:
            width = len(line)
            empty_cols = set(range(width))
        lines.append(line)
        height += 1
        # Do the row expansions on the way through
        if all([x == '.' for x in line]):
            print(f"Expanding row {height}")
            lines.append('|' * width)
            height += 1
        else:
            # Prep for column expansions
            empty_cols -= {i for i, x in enumerate(line) if x == '#'}

    # Expand the empty columns
    empty_cols = list(empty_cols)
    empty_cols.sort()
    print(f"Expanding columns {empty_cols}")
    for i, line in enumerate(lines):
        expansions = 0
        for col in empty_cols:
            j = col + expansions
            line = line[:j] + '-' + line[j:]
            expansions += 1
        lines[i] = line
    width += expansions

    print('\n'.join(lines))
    galaxies = []
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == '#':
                galaxies.append((i, j))

    print(f"Got {len(galaxies)} galaxies on a {width} x {height} field")
    pairs = list(combinations(galaxies, 2))
    total = 0
    for a, b in pairs:
        dist = get_distance(a, b)
        total += dist
    print(total)
