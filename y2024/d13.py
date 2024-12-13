"""Advent of Code 2024

Day 13: Claw Contraption

https://adventofcode.com/2024/day/13
"""
import logging  # noqa: F401
import re

from util import timing, INF


BUTTON_PATTERN = re.compile(r'Button \w: X\+(\d+), Y\+(\d+)')
PRIZE_PATTERN = re.compile(r'Prize: X=(\d+), Y=(\d+)')


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


def find_solution(machine) -> tuple | None:
    ax, ay, bx, by, px, py = machine
    best = INF
    for a in range(101):
        x = a * ax
        remain = px - x
        div, mod = divmod(remain, bx)
        if mod == 0 and div <= 100:
            # Found a solution for X, does it also work for Y?
            b = div
            if (a * ay + b * by) == py:
                cost = get_cost(a, b)
                if cost < best:
                    best = cost
    return best if best < INF else None


def get_best_total_cost(machines) -> int:
    return sum(find_solution(x) or 0 for x in machines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_best_total_cost(parsed)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
