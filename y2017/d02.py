"""Advent of Code 2017

Day 2: Corruption Checksum

https://adventofcode.com/2017/day/2
"""
import logging
from itertools import permutations


def parse(stream) -> tuple:
    rows = []
    for line in stream:
        values = line.split()
        rows.append(tuple(map(int, values)))
    logging.debug(rows)
    return rows


def get_checksum(rows: tuple) -> int:
    """Return the checksum of the spreadsheet.

    This is equal to the sum of the difference between the largest and smallest
    values of each row.
    """
    result = 0
    for row in rows:
        diff = max(row) - min(row)
        result += diff
    return result


def get_divisible_sum(rows: tuple) -> int:
    """Return the sum of evenly divisible numbers from each row."""
    result = 0
    for row in rows:
        for a, b in permutations(row, 2):
            if a % b == 0:
                result += a // b
                break
    return result


def run(stream, test=False):
    rows = parse(stream)
    result1 = get_checksum(rows)
    result2 = get_divisible_sum(rows)

    return (result1, result2)
