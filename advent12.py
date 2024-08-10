#!/usr/bin/env python
import re
import sys
import time
from contextlib import contextmanager


RUN_RE = re.compile(r'[#?]+')
REGEX_TIMINGS = []
FUNC_TIMINGS = []


@contextmanager
def timing(accumulator=None):
    try:
        start = time.perf_counter_ns()
        yield start
    finally:
        duration = time.perf_counter_ns() - start
        if accumulator is not None:
            accumulator.append(duration)


def replace(source: str, position: int, replacement: str):
    return source[:position] + replacement + source[position + 1:]


def check_row(row: str, runs: tuple[int]) -> bool:
    """Check whether a row matches its run series."""
    runs = list(runs)
    in_run = False
    current_run = None
    run_size = 0
    for ch in row:
        if ch == '#':
            if not in_run:
                in_run = True
                current_run = runs.pop(0)
                run_size = 1
            else:
                run_size += 1
                if run_size > current_run:
                    return False
        elif in_run:
            if run_size != current_run:
                return False
            in_run = False
    if in_run and run_size != current_run:
        return False

    return True


def check_pattern(pattern: str, row: str) -> bool:
    """Check whether a row matches its original pattern."""
    assert len(pattern) == len(row)
    for i, ch in enumerate(pattern):
        if ch != '?' and ch != row[i]:
            return False
    return True


def count_ways(
        row: str,
        runs: tuple[int],
        regex: re.Pattern = None,
        firstpass: bool = True) -> int:
    indexes = [i for i, x in enumerate(row) if x == '?']
    unknown = len(indexes)
    total = sum(runs)
    missing = total - row.count('#')
    if unknown == missing or missing == 0:
        return 1

    if not regex:
        run_pattern = r'[.?]+'.join([f'[#?]{{{x}}}' for x in runs])
        regex = re.compile(r'[.?]*' + run_pattern + r'[.?]*')

    # First pass: replace unknowns that have only one valid solution
    if firstpass:
        for i in indexes:
            with_hash = replace(row, i, '#')
            with_dot = replace(row, i, '.')
            hash_ok = regex.fullmatch(with_hash)
            dot_ok = regex.fullmatch(with_dot)

            if dot_ok and not hash_ok:
                row = with_dot
            if hash_ok and not dot_ok:
                row = with_hash

    # Second pass: recurse into each valid solution
    indexes = [i for i, x in enumerate(row) if x == '?']
    unknown = len(indexes)
    missing = total - row.count('#')
    if unknown == missing or missing == 0:
        return 1

    i = indexes[0]
    result = 0
    for ch in ('#', '.'):
        attempt = replace(row, i, ch)
        valid = regex.fullmatch(attempt)
        if valid:
            result += count_ways(attempt, runs, regex, False)
    return result


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append([field, runs])

    # Part 1
    total = 0
    for row, runs in rows:
        print(f"{row} {runs}")
        ways = count_ways(row, runs)
        total += ways
        print(f"{ways}")
    print(total)

    # Part 2 - expand all inputs rows by 5x
    for i, [row, runs] in enumerate(rows):
        rows[i][0] = '?'.join([row] * 5)
        rows[i][1] = runs * 5

    total = 0
    for row, runs in rows:
        ways = count_ways(row, runs)
        total += ways
    print(total)
