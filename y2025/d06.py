"""Advent of Code 2025

Day 6: Trash Compactor

https://adventofcode.com/2025/day/6
"""
import logging  # noqa: F401
from collections import defaultdict
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


def solve_problem(problem):
    fn = add if problem[-1] == '+' else mul
    return reduce(fn, problem[:-1])


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum([solve_problem(x) for x in parsed.values()])

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
