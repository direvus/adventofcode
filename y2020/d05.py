"""Advent of Code 2020

Day 5: Binary Boarding

https://adventofcode.com/2020/day/5
"""
import logging  # noqa: F401

from util import timing


def get_seat(passid: str) -> tuple:
    """Return the seat indicated by this boarding pass.

    The return value is a tuple in (row, column) format.
    """
    low = 0
    high = 127
    for i in range(7):
        diff = (high - low + 1) // 2
        if passid[i] == 'F':
            high -= diff
        else:
            low += diff
    row = high

    low = 0
    high = 7
    for i in range(7, 10):
        diff = (high - low + 1) // 2
        if passid[i] == 'L':
            high -= diff
        else:
            low += diff
    col = high

    return (row, col)


def get_seat_id(passid: str) -> int:
    row, col = get_seat(passid)
    return row * 8 + col


def get_seat_ids(passids: tuple[str]) -> set[int]:
    result = set()
    for passid in passids:
        result.add(get_seat_id(passid))
    return result


def get_missing_seatid(seatids: set[int]) -> int:
    for i in range(128 * 8):
        if i not in seatids and i - 1 in seatids and i + 1 in seatids:
            return i


def parse(stream) -> tuple[str]:
    result = []
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        result.append(line)
    return tuple(result)


def run(stream, test: bool = False):
    with timing("Part 1"):
        passids = parse(stream)
        seatids = get_seat_ids(passids)
        result1 = max(seatids)

    with timing("Part 2"):
        result2 = get_missing_seatid(seatids)

    return (result1, result2)
