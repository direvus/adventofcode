"""Advent of Code 2024

Day 13: Claw Contraption

https://adventofcode.com/2024/day/13
"""
import logging  # noqa: F401
import re

from matrix import solve_gaussian
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
    a, b = solve_gaussian(matrix)
    if a.denominator == 1 and b.denominator == 1:
        logging.debug(f'{machine} -> A = {a}, B = {b}')
        a = a.numerator
        b = b.numerator
        return get_cost(a, b)
    return None


def get_best_total_cost(machines) -> int:
    return sum(find_solution(x) or 0 for x in machines)


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
