"""Advent of Code 2019

Day 9: Sensor Boost

https://adventofcode.com/2019/day/9
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


def parse(stream) -> Computer:
    return Computer(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        comp.add_input(1)
        result1 = ','.join(str(x) for x in comp.run())

    with timing("Part 2"):
        comp2 = comp.clone()
        comp2.add_input(2)
        result2 = ','.join(str(x) for x in comp2.run())

    return (result1, result2)
