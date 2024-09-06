#!/usr/bin/env python
from util import timing


def has_reflection(rows: list[str], position: int) -> bool:
    n = min(position, len(rows) - position)
    for i in range(1, n + 1):
        if rows[position - i] != rows[position + i - 1]:
            return False
    return True


def count_differences(rows: list[str], position: int) -> int:
    n = min(position, len(rows) - position)
    result = 0
    for i in range(1, n + 1):
        a = rows[position - i]
        b = rows[position + i - 1]
        for j, ch in enumerate(a):
            if ch != b[j]:
                result += 1
    return result


def find_reflection(rows: list[str], tolerance: int = 0) -> int:
    for i in range(1, len(rows)):
        if tolerance == 0:
            if has_reflection(rows, i):
                return i
        else:
            diff = count_differences(rows, i)
            if diff == tolerance:
                return i
    return 0


def pivot(rows: list[str]) -> list[str]:
    """Translate columns into rows."""
    result = []
    for i in range(len(rows[0])):
        col = ''.join([row[i] for row in rows])
        result.append(col)
    return result


def detect_reflections(rows: list[str], tolerance: int = 0) -> tuple[int]:
    h = find_reflection(rows, tolerance)

    verticals = pivot(rows)
    v = find_reflection(verticals, tolerance)

    return (h, v)


def run(stream, test=False):
    patterns = []
    rows = []
    for line in stream:
        row = line.strip()
        if row:
            rows.append(row)
        elif rows:
            patterns.append(rows)
            rows = []
    if rows:
        patterns.append(rows)

    # Part 1
    total1 = 0
    with timing("Part 1"):
        for pattern in patterns:
            h, v = detect_reflections(pattern, 0)
            total1 += v + (100 * h)
    print(f"Total for Part 1 = {total1}\n")

    # Part 2
    total2 = 0
    with timing("Part 2"):
        for pattern in patterns:
            h, v = detect_reflections(pattern, 1)
            total2 += v + (100 * h)
    print(f"Total for Part 2 = {total2}\n")
    return (total1, total2)
