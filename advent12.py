#!/usr/bin/env python
import re
import sys
from itertools import combinations


RUN_RE = re.compile(r'[#?]+')


def count_ways(row: str, runs: tuple[int]) -> int:
    unknown = row.count('?')
    total = sum(runs)
    missing = total - row.count('#')
    if unknown == missing:
        return 1

    indexes = [i for i, x in enumerate(row) if x == '?']
    ways = 0
    for comb in combinations(indexes, missing):
        attempt = ''.join([
                x if i not in indexes else '#' if i in comb else '.'
                for i, x in enumerate(row)])
        parts = RUN_RE.findall(attempt)
        lengths = tuple((len(x) for x in parts))
        if lengths == runs:
            ways += 1
    return ways


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append((field, runs))

    total = 0
    for row, runs in rows:
        total += count_ways(row, runs)
    print(total)
