"""Advent of Code 2017

Day 17: Spinlock

https://adventofcode.com/2017/day/17
"""
import logging  # noqa: F401

from util import timing, jit


COUNT1 = 2017
COUNT2 = 50 * 10 ** 6


class Node:
    def __init__(self, value: int, nextnode: 'Node' = None):
        self.value = value
        self.next = nextnode


def create_list(values: list):
    assert len(values) > 0
    start = Node(values[0])
    prev = start
    for value in values[1:]:
        node = Node(value)
        prev.next = node
        prev = node
    prev.next = start
    return start


def get_list_values(start: Node) -> list:
    result = [start.value]
    if start.next is start:
        return result
    node = start
    while node.next is not start:
        node = node.next
        result.append(node.value)
    return result


def update_list(current: Node, steps: int) -> Node:
    """Update the list for one iteration.

    Seek forward through the list `steps` times, then insert a new node and
    return it.
    """
    value = current.value
    if current.next is current:
        node = Node(value + 1, current)
        current.next = node
        return node

    for _ in range(steps):
        current = current.next
    post = current.next
    node = Node(value + 1, post)
    current.next = node
    return node


def get_final_value(steps: int, count: int) -> int:
    node = create_list([0])
    for _ in range(count):
        node = update_list(node, steps)
    return node.next.value


@jit
def get_value_after_zero(steps: int, count: int) -> int:
    """Update the buffer `count` times and return the value after zero."""
    size = 1
    position = 0
    value = 0
    result = 0
    for i in range(count):
        value += 1
        position = ((position + steps) % size) + 1
        if position == 1:
            result = value
        size += 1

    return result


def parse(stream) -> tuple:
    return int(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        steps = parse(stream)
        result1 = get_final_value(steps, COUNT1)

    with timing("Part 2"):
        result2 = get_value_after_zero(steps, COUNT2)

    return (result1, result2)
