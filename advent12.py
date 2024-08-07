#!/usr/bin/env python
import re
import sys
from itertools import combinations


RUN_RE = re.compile(r'[#?]+')


def replace(source: str, position: int, replacement: str):
    return source[:position] + replacement + source[position + 1:]


def simplify(row: str, runs: tuple[int]) -> str:
    """Simplify a row by eliminating impossible options.

    We iterate through each of the unknown positions (marked with ?) and try
    substituting in a dot, and a hash. If only one of those substitutions still
    fits the run pattern, we can resolve the unknown marker and replace it
    permanently with a dot or a hash.
    """
    indexes = tuple((i for i, x in enumerate(row) if x == '?'))
    run_pattern = r'[.?]+'.join([f'[#?]{{{x}}}' for x in runs])
    rex = re.compile(r'[.?]*' + run_pattern + r'[.?]*')

    for i in indexes:
        with_hash = replace(row, i, '#')
        with_dot = replace(row, i, '.')
        hash_ok = rex.fullmatch(with_hash)
        dot_ok = rex.fullmatch(with_dot)

        if dot_ok and not hash_ok:
            row = with_dot
        if hash_ok and not dot_ok:
            row = with_hash
    return row


def count_ways(row: str, runs: tuple[int]) -> int:
    unknown = row.count('?')
    total = sum(runs)
    missing = total - row.count('#')
    if unknown == missing or missing == 0:
        return 1

    print(f"{row} {runs}")
    row = simplify(row, runs)
    indexes = [i for i, x in enumerate(row) if x == '?']
    unknown = len(indexes)
    missing = total - row.count('#')
    if unknown == missing or missing == 0:
        return 1

    rex = re.compile(r'\.*' + r'\.+'.join(['#' * x for x in runs]) + r'\.*')
    ways = 0
    for comb in combinations(indexes, missing):
        attempt = ''.join([
                x if i not in indexes else '#' if i in comb else '.'
                for i, x in enumerate(row)])
        if rex.fullmatch(attempt):
            ways += 1
    print(f"   {ways} ways")
    return ways


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append([field, runs])

    # Part 1
    total = 0
    for row, runs in rows:
        total += count_ways(row, runs)
    print(total)

    # Part 2 - expand all inputs rows by 5x
    for i, [row, runs] in enumerate(rows):
        rows[i][0] = '?'.join([row] * 5)
        rows[i][1] = runs * 5

    total = 0
    for row, runs in rows:
        total += count_ways(row, runs)
    print(total)
