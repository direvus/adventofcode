"""Advent of Code 2019

Day 5: Sunny with a Chance of Asteroids

https://adventofcode.com/2019/day/5
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
        outputs = comp.run((1,))
        result1 = outputs[-1]

    with timing("Part 2"):
        comp.reset()
        outputs = comp.run((5,))
        result2 = outputs[0]

    return (result1, result2)
