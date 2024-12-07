"""Advent of Code 2024

Day 7: Bridge Repair

https://adventofcode.com/2024/day/7
"""
import logging  # noqa: F401
from collections import deque
from operator import add, mul

from util import timing


def concat_int(a: int, b: int) -> int:
    return int(f'{a}{b}')


OPS = frozenset({add, mul})
OPS2 = frozenset(OPS | {concat_int})


def parse(stream) -> str:
    result = []
    for line in stream:
        left, right = line.strip().split(': ')
        output = int(left)
        operands = tuple(map(int, right.split()))
        result.append((output, operands))
    return result


def is_solvable(target, operands, operations):
    q = deque()
    q.append((operands[0], operands[1:]))
    while q:
        state, remain = q.pop()
        if state > target:
            continue

        if not remain:
            if state == target:
                return True
            continue

        for op in operations:
            q.append((op(state, remain[0]), remain[1:]))
    return False


def get_calibration(records, operations):
    return sum(x[0] if is_solvable(*x, operations) else 0 for x in records)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_calibration(parsed, OPS)

    with timing("Part 2"):
        result2 = get_calibration(parsed, OPS2)

    return (result1, result2)
