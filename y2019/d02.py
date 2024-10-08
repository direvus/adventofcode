"""Advent of Code 2019

Day 2: 1202 Program Alarm

https://adventofcode.com/2019/day/2
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


def parse(stream) -> Computer:
    comp = Computer()
    comp.parse(stream)
    return comp


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        if test:
            comp.run()
        else:
            comp.memory[1] = 12
            comp.memory[2] = 2
            comp.run()
        result1 = comp.memory[0]

    with timing("Part 2"):
        if test:
            result2 = 0
        else:
            target = 19690720
            noun, verb = comp.find_inputs(target)
            result2 = noun * 100 + verb

    return (result1, result2)
