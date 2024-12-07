"""Advent of Code 2024

Day 7: Bridge Repair

https://adventofcode.com/2024/day/7
"""
import logging  # noqa: F401
from itertools import product
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


def evaluate(target, operands, operations):
    result = operands[0]
    for i, op in enumerate(operations):
        result = op(result, operands[i + 1])
        if result > target:
            return result
    return result


def is_solvable(target, operands, operations):
    count = len(operands) - 1
    for sequence in product(operations, repeat=count):
        result = evaluate(target, operands, sequence)
        if result == target:
            return True
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
