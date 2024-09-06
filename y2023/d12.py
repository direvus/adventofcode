#!/usr/bin/env python
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


def run(stream, test=False):
    rows = []
    for line in stream:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append([field, runs])

    # Part 1
    total1 = 0
    part1 = []
    with timing("Part 1"):
        for row, runs in rows:
            nways = count_ways_slide(row, runs)
            total1 += nways
            part1.append(nways)
    print(f"Total ways for Part 1 = {total1}\n")

    # Part 2
    total2 = 0
    for i, nways in enumerate(part1):
        with timing(f"Row {i + 1}"):
            orig_row, orig_runs = rows[i]
            row = '?'.join([orig_row] * 5)
            subtotal = count_ways_slide(row, orig_runs * 5)
            total2 += subtotal
        print(f"Row {i+1} = {subtotal}")
    return (total1, total2)
