#!/usr/bin/env python
import sys

from util import timing, Direction


def get_total_load(pattern: list[list]) -> int:
    result = 0
    i = 1
    for row in reversed(pattern):
        result += row.count('O') * i
        i += 1
    return result


def pivot(rows: list[list]) -> list[list]:
    """Translate columns into rows."""
    return [[row[x] for row in rows] for x in range(len(rows[0]))]


def flip(rows: list[list]) -> list[list]:
    """Reverse every row."""
    return [list(reversed(x)) for x in rows]


def slide_rocks(row: list) -> list:
    """Slide all rocks in `row` as far WEST as possible."""
    space = 0
    rocks = 0
    start = 0
    row = list(row)
    for i, ch in enumerate(row):
        if ch == '.':
            space += 1
        elif ch == 'O':
            rocks += 1
        else:
            if rocks and space:
                part = ['O'] * rocks + ['.'] * space
                end = start + rocks + space
                row = row[:start] + part + row[end:]
            start = i + 1
            space = 0
            rocks = 0
    if rocks and space:
        part = ['O'] * rocks + ['.'] * space
        end = start + rocks + space
        row = row[:start] + part + row[end:]
    return row


def rotate(
        rows: list[list],
        direction: Direction,
        reverse: bool = False,
        ) -> list[list]:
    if direction == Direction.NORTH:
        return pivot(rows)
    if direction == Direction.EAST:
        return flip(rows)
    if direction == Direction.SOUTH:
        if reverse:
            return pivot(flip(rows))
        else:
            return flip(pivot(rows))
    # West doesn't need any transformation
    return rows


def tilt(rows: list[list], direction: Direction) -> list[list]:
    rotated = rotate(rows, direction)
    result = []
    for i, row in enumerate(rotated):
        result.append(slide_rocks(row))
    return rotate(result, direction, reverse=True)


def to_string(rows: list[list]) -> str:
    return '\n'.join([''.join(row) for row in rows])


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        row = list(line.strip())
        if row:
            rows.append(row)

    # Part 1
    with timing("Part 1"):
        tilted = tilt(rows, Direction.NORTH)
        load = get_total_load(tilted)
    print(f"Result for Part 1 = {load}\n")

    # Part 2
    results = []
    limit = 1000000000
    with timing("Part 2\n"):
        cycles = 0
        results.append(rows)
        while cycles < limit:
            rows = tilt(rows, Direction.NORTH)
            rows = tilt(rows, Direction.WEST)
            rows = tilt(rows, Direction.SOUTH)
            rows = tilt(rows, Direction.EAST)
            if rows == results[-1]:
                # If it's the same every cycle, no need to keep going
                break
            cycles += 1
            matches = [i for i, x in enumerate(results) if x == rows]
            if matches:
                # Loop detected
                start = matches[0]
                diff = cycles - start
                print(
                    f"Cycle {cycles} matched {start} -- "
                    f"looping every {diff} cycles")
                index = ((limit - start) % diff) + start
                if index < cycles:
                    rows = results[index]
                    print(f"Found target result at {index}")
                    break
                limit = index
                print(f"Continuing until we get to {index} ...")
            results.append(rows)
        load = get_total_load(rows)
    print(f"Result for Part 2 = {load}\n")
