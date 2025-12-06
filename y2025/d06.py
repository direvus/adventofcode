"""Advent of Code 2025

Day 6: Trash Compactor

https://adventofcode.com/2025/day/6
"""
import logging  # noqa: F401
from collections import defaultdict, deque
from functools import reduce
from operator import add, mul

from util import timing


def parse(stream) -> str:
    problems = defaultdict(list)
    for line in stream:
        line = line.strip()
        parts = line.split()
        for i, part in enumerate(parts):
            if part not in '*+':
                part = int(part)
            problems[i].append(part)
    return problems


def parse_p2(lines):
    cols = defaultdict(list)
    operators = deque()
    width = 0
    for line in lines:
        width = max(width, len(line))
        if line[0] in '*+':
            operators.extend(line.split())
        else:
            for i, c in enumerate(line):
                if c.isdigit():
                    cols[i].append(c)
    problems = []
    numbers = []
    for i in range(width):
        if numbers and i not in cols:
            numbers.append(operators.popleft())
            problems.append(numbers)
            numbers = []
            continue
        n = int(''.join(cols[i]))
        numbers.append(n)

    if numbers:
        numbers.append(operators.popleft())
        problems.append(numbers)

    return problems


def solve_problem(problem):
    fn = add if problem[-1] == '+' else mul
    return reduce(fn, problem[:-1])


def run(stream, test: bool = False):
    # Need to capture the full input so that we can parse it differently for
    # Part 2.
    lines = [x for x in stream]
    with timing("Part 1"):
        parsed = parse(lines)
        result1 = sum([solve_problem(x) for x in parsed.values()])

    with timing("Part 2"):
        parsed = parse_p2(lines)
        result2 = sum([solve_problem(x) for x in parsed])

    return (result1, result2)
