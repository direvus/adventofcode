"""Advent of Code 2019

Day 19: Tractor Beam

https://adventofcode.com/2019/day/19
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


def parse(stream) -> Computer:
    return Computer(stream.readline().strip())


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        comp = parse(stream)

        result1 = 0
        lines = []
        for y in range(50):
            line = []
            for x in range(50):
                comp.reset()
                comp.add_inputs((x, y))
                value = next(comp.generate())
                result1 += value
                line.append('#' if value else '.')
            lines.append(''.join(line))
        print('\n'.join(lines))

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
