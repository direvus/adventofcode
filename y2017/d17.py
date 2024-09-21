"""Advent of Code 2017

Day 17: Spinlock

https://adventofcode.com/2017/day/17
"""
import logging  # noqa: F401

from util import timing


COUNT1 = 2017
COUNT2 = 50 * 10 ** 6


def create_list(value: int):
    node = [value, None]
    node[1] = node
    return node


def get_list_values(start: list) -> list:
    result = [start[0]]
    if start[1] is start:
        return result
    node = start
    while not node[1] is start:
        node = node[1]
        result.append(node[0])
    return result


def update_list(current: list, steps: int) -> list:
    """Update the list for one iteration.

    Seek forward through the list `steps` times, then insert a new node and
    return it.
    """
    value = current[0]
    if current[1] is current:
        node = [value + 1, current]
        current[1] = node
        return node

    for _ in range(steps):
        current = current[1]
    post = current[1]
    node = [value + 1, post]
    current[1] = node
    return node


def get_final_value(steps: int, count: int) -> int:
    node = create_list(0)
    for _ in range(count):
        node = update_list(node, steps)
    return node[1][0]


def get_value_after_zero(steps: int, count: int) -> int:
    """Update the buffer `count` times and return the value after zero."""
    node = create_list(0)
    for i in range(count):
        node = update_list(node, steps)

    while node[0] != 0:
        node = node[1]
    return node[1][0]


def parse(stream) -> tuple:
    return int(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        steps = parse(stream)
        result1 = get_final_value(steps, COUNT1)

    with timing("Part 2"):
        count = 9 if test else COUNT2
        result2 = get_value_after_zero(steps, count)

    return (result1, result2)
