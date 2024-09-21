"""Advent of Code 2017

Day 17: Spinlock

https://adventofcode.com/2017/day/17
"""
import logging  # noqa: F401

from util import timing


COUNT1 = 2017
COUNT2 = 50 * 10 ** 6


def update_buffer(values: list, position: int, steps: int) -> list:
    """Update the buffer for one iteration.

    Modifies the buffer list in-place and returns the new position.
    """
    value = values[position]
    position = (position + steps) % len(values) + 1
    values.insert(position, value + 1)
    return position


def get_final_value(steps: int, count: int) -> int:
    buffer = [0]
    position = 0
    for _ in range(count):
        position = update_buffer(buffer, position, steps)
    position = (position + 1) % len(buffer)
    return buffer[position]


def get_value_after_zero(steps: int, count: int) -> int:
    """Update the buffer `count` times and return the value after zero."""
    buffer = [0]
    position = 0
    for _ in range(count):
        value = buffer[position]
        position = (position + steps) % len(buffer) + 1
        buffer.insert(position, value + 1)
    index = buffer.index(0)
    return buffer[(index + 1) % len(buffer)]


def parse(stream) -> tuple:
    return int(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        steps = parse(stream)
        result1 = get_final_value(steps, COUNT1)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
