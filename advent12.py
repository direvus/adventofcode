#!/usr/bin/env python
import sys

from util import timing


COUNTS = {}


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
        if not valid:
            block = '.' + block
            length += 1
            continue
        if nruns > 1:
            remain = row[len(block):]
            ways = count_ways_slide(remain, runs[1:])
            result += ways
        elif '#' not in row[len(block):]:
            result += 1
        block = '.' + block
        length += 1

    COUNTS.setdefault(row, {})[runs] = result
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
    total = 0
    for i, nways in enumerate(part1):
        with timing(f"Row {i + 1}"):
            orig_row, orig_runs = rows[i]
            row = '?'.join([orig_row] * 5)
            subtotal = count_ways_slide(row, orig_runs * 5)
            total += subtotal
        print(f"Row {i+1} = {subtotal}")
    print(total)
