"""Advent of Code 2017

Day 5: A Maze of Twisty Trampolines, All Alike

https://adventofcode.com/2017/day/5
"""
import logging

from util import timing


def parse(stream) -> list[int]:
    return [int(line.strip()) for line in stream]


def count_steps(jumps: list[int], part: int = 1) -> int:
    counter = 0
    pointer = 0
    while pointer >= 0 and pointer < len(jumps):
        jump = jumps[pointer]
        jumps[pointer] += 1 if part == 1 or jump < 3 else -1
        logging.debug(jumps)
        pointer += jump
        counter += 1
    return counter


def run(stream, test=False):
    jumps = parse(stream)
    with timing("Part 1"):
        result1 = count_steps(list(jumps), 1)
    with timing("Part 2"):
        result2 = count_steps(jumps, 2)

    return (result1, result2)
