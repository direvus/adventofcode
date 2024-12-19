"""Advent of Code 2024

Day 19: Linen Layout

https://adventofcode.com/2024/day/19
"""
import logging  # noqa: F401
from collections import deque
from functools import cache

from util import timing


def parse(stream) -> str:
    line = stream.readline().strip()
    towels = tuple(line.split(', '))
    # consume a blank line
    stream.readline()
    # all remaining lines are designs
    designs = [x.strip() for x in stream]
    return towels, designs


def is_possible(design, towels) -> bool:
    q = deque()
    q.append('')
    # Remove all the towels that don't appear anywhere in the design
    towels = [x for x in towels if x in design]
    # Prioritise the longest towels
    towels.sort(key=lambda x: len(x))
    while q:
        s = q.pop()
        if s == design:
            return True
        remain = design[len(s):]
        for towel in towels:
            if remain.startswith(towel):
                q.append(s + towel)
    return False


@cache
def count_solutions(design, towels) -> int:
    if design == '':
        return 1

    result = 0
    for towel in towels:
        if design.startswith(towel):
            remain = design[len(towel):]
            result += count_solutions(remain, towels)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        towels, designs = parse(stream)
        possible = {d for d in designs if is_possible(d, towels)}
        result1 = len(possible)

    with timing("Part 2"):
        result2 = sum(count_solutions(d, towels) for d in possible)

    return (result1, result2)
