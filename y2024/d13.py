"""Advent of Code 2024

Day 13: Claw Contraption

https://adventofcode.com/2024/day/13
"""
import logging  # noqa: F401
import re
from fractions import Fraction

from util import timing


BUTTON_PATTERN = re.compile(r'Button \w: X\+(\d+), Y\+(\d+)')
PRIZE_PATTERN = re.compile(r'Prize: X=(\d+), Y=(\d+)')
PART2_ADD = 10000000000000


def parse(stream) -> str:
    result = []
    data = stream.read()
    blocks = data.split('\n\n')
    for block in blocks:
        lines = block.split('\n')
        ax, ay = BUTTON_PATTERN.search(lines[0]).groups()
        bx, by = BUTTON_PATTERN.search(lines[1]).groups()
        px, py = PRIZE_PATTERN.search(lines[2]).groups()
        result.append(tuple(map(int, (ax, ay, bx, by, px, py))))
    return result


def get_cost(a, b) -> int:
    return a * 3 + b


def find_solution(machine) -> int | None:
    matrix = get_matrix_form(machine)
    a, b = eliminate(matrix)
    if a.denominator == 1 and b.denominator == 1:
        logging.debug(f'{machine} -> A = {a}, B = {b}')
        a = a.numerator
        b = b.numerator
        return get_cost(a, b)
    return None


def get_best_total_cost(machines) -> int:
    return sum(find_solution(x) or 0 for x in machines)


def num_leading_zeros(row: list) -> int:
    for i, n in enumerate(row):
        if n != 0:
            return i
    return i + 1


def get_non_echelon_row(matrix: list) -> int:
    prev = -1
    for i, row in enumerate(matrix):
        z = num_leading_zeros(row)
        if z == len(row):
            return None
        if z <= prev:
            return i
        prev = z
    return None


def scale_iter(v, f):
    return tuple((x * f for x in v))


def eliminate(matrix: list) -> list:
    """Perform a Gaussian elimination on an augmented matrix.

    Return the list of values in the solution, or raise an exception if a
    unique solution cannot be found.
    """
    while True:
        matrix.sort(key=num_leading_zeros)
        i = get_non_echelon_row(matrix)
        if i is None:
            break
        j = num_leading_zeros(matrix[i])
        upper = matrix[i - 1]
        for i in range(i, len(matrix)):
            lead = matrix[i][j]
            if lead == 0:
                break
            factor = Fraction(0 - lead, upper[j])
            scaled = scale_iter(upper, factor)
            matrix[i] = tuple(map(lambda a, b: a + b, matrix[i], scaled))

    width = len(matrix[0]) - 1
    solution = [None] * width
    for row in reversed(matrix):
        z = num_leading_zeros(row)
        aug = row[width]
        for j in range(z + 1, width):
            aug -= row[j] * solution[j]
        solution[z] = Fraction(aug, row[z])
    return solution


def get_matrix_form(machine) -> list:
    ax, ay, bx, by, px, py = machine
    return [
            (ax, bx, px),
            (ay, by, py),
            ]


def transform_part2(machine) -> tuple:
    ax, ay, bx, by, px, py = machine
    return (ax, ay, bx, by, px + PART2_ADD, py + PART2_ADD)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_best_total_cost(parsed)

    with timing("Part 2"):
        machines2 = tuple(map(transform_part2, parsed))
        result2 = get_best_total_cost(machines2)

    return (result1, result2)
