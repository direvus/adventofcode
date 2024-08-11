#!/usr/bin/env python
import sys

from util import timing


def get_total_load(pattern: list[str]) -> int:
    result = 0
    i = 1
    for row in reversed(pattern):
        result += row.count('O') * i
        i += 1
    return result


def pivot(rows: list[str]) -> list[str]:
    """Translate columns into rows."""
    result = []
    for i in range(len(rows[0])):
        col = ''.join([row[i] for row in rows])
        result.append(col)
    return result


def slide_rocks(row: str) -> str:
    space = 0
    rocks = 0
    start = 0
    for i, ch in enumerate(row):
        if ch == '.':
            space += 1
        elif ch == 'O':
            rocks += 1
        else:
            if rocks and space:
                part = 'O' * rocks + '.' * space
                end = start + rocks + space
                row = row[:start] + part + row[end:]
            start = i + 1
            space = 0
            rocks = 0
    if rocks and space:
        part = 'O' * rocks + '.' * space
        end = start + rocks + space
        row = row[:start] + part + row[end:]
    return row


def tilt(rows: list[str]) -> list[str]:
    flipped = pivot(rows)
    for i, row in enumerate(flipped):
        flipped[i] = slide_rocks(row)
    return pivot(flipped)


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        row = line.strip()
        if row:
            rows.append(row)

    # Part 1
    with timing("Part 1"):
        tilted = tilt(rows)
        load = get_total_load(tilted)
    print(f"Result for Part 1 = {load}\n")
