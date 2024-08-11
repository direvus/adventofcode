#!/usr/bin/env python
import re
import sys
import time
from contextlib import contextmanager


COUNTS = {}


@contextmanager
def timing(message: str = None) -> int:
    start = time.perf_counter_ns()
    if message:
        print(f"[......] {message}", end='')
    try:
        yield start
    finally:
        end = time.perf_counter_ns()
        dur = end - start
        print(f"\r\033[2K[{dur//1000:6d}] {message}")


def replace(source: str, position: int, replacement: str):
    return source[:position] + replacement + source[position + 1:]


def build_regex(runs: tuple[int]) -> re.Pattern:
    run_pattern = r'[.?]+'.join([f'[#?]{{{x}}}' for x in runs])
    return re.compile(r'[.?]*' + run_pattern + r'[.?]*')


def simplify(row: str, regex: re.Pattern) -> str:
    indexes = [i for i, x in enumerate(row) if x == '?']
    for i in indexes:
        with_hash = replace(row, i, '#')
        with_dot = replace(row, i, '.')
        hash_ok = regex.fullmatch(with_hash)
        dot_ok = regex.fullmatch(with_dot)

        if dot_ok and not hash_ok:
            row = with_dot
        if hash_ok and not dot_ok:
            row = with_hash
    return row


def get_lead_space(row: str) -> int:
    for i, ch in enumerate(row):
        if ch not in {'#', '.'}:
            return i
    return i


def is_block_valid(row: str, block: str) -> bool:
    for i, ch in enumerate(block):
        p = row[i]
        if p != ch and p != '?':
            return False
    return True


def count_ways_slide(row: str, runs: tuple[int]) -> int:
    runsets = COUNTS.get(row, {})
    if runs in runsets:
        return runsets[runs]

    result = 0
    nruns = len(runs)
    length = sum(runs) + nruns - 1
    run = runs[0]
    block = '#' * run
    if nruns > 1:
        block += '.'
    while length <= len(row):
        valid = is_block_valid(row, block)
        #print(f"  {block} in {row} is {valid}")
        if not valid:
            block = '.' + block
            length += 1
            continue
        if nruns > 1:
            remain = row[len(block):]
            #print(f"  Recursing with {remain}")
            ways = count_ways_slide(remain, runs[1:])
            result += ways
        elif '#' not in row[len(block):]:
            result += 1
        block = '.' + block
        length += 1

    COUNTS.setdefault(row, {})[runs] = result
    #print(f"  Return {result} for {row} {runs}")
    return result


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append([field, runs])

    # Part 1
    total = 0
    part1 = []
    with timing("Part 1"):
        for row, runs in rows:
            nways = count_ways_slide(row, runs)
            total += nways
            part1.append(nways)
    print(f"Total ways for Part 1 = {total}\n")

    # Part 2
    #
    # We already know all the ways the expanded row can be solved WITHOUT using
    # the new '?' delimiters - we just need to check all the ways it can be
    # solved where we do use at least one of them.
    total = 0
    for i, nways in enumerate(part1):
        with timing(f"Row {i + 1}"):
            orig_row, orig_runs = rows[i]
            h = []
            row = orig_row
            runs = orig_runs
            for n in range(4):
                row = row + '#' + orig_row
                runs = runs + orig_runs
                with timing(f"Count ways for row {i + 1} x {n + 2}"):
                    ways = count_ways_slide(row, runs)
                h.append(ways)
            subtotal = sum([
                    nways ** 5,
                    4 * h[0] * (nways ** 3),
                    3 * h[1] * (nways ** 2),
                    2 * h[2] * nways,
                    3 * (h[0] ** 2) * nways,
                    2 * h[0] * h[1],
                    h[3],
                    ])
            total += subtotal
        print(f"Row {i+1} = {subtotal}")
    print(total)
