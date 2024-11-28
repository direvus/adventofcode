"""Advent of Code 2022

Day 20: Grove Positioning System

https://adventofcode.com/2022/day/20
"""
import logging  # noqa: F401

from util import timing


class Node:
    def __init__(self, value, head=None, tail=None):
        self.value = value
        self.head = head
        self.tail = tail


class Mixer:
    def __init__(self, values):
        self.zero = None
        self.size = 0
        self.index = {}
        self.values = []

        last = None

        for value in values:
            node = Node(value, last)
            if last:
                last.tail = node
            else:
                first = node
            self.size += 1
            if value == 0:
                self.zero = node
            self.values.append(node)
            last = node
        first.head = last
        last.tail = first

    def shift_node(self, node):
        value = node.value
        if value == 0:
            return

        head = node.head
        tail = node.tail
        # remove the node from its current position
        head.tail = tail
        tail.head = head

        if value > 0:
            pos = tail
            for _ in range(value):
                pos = pos.tail
        else:
            pos = head
            for _ in range(abs(value) - 1):
                pos = pos.head

        # insert the node back into the list at this new position
        head = pos.head
        pos.head = node
        head.tail = node
        node.head = head
        node.tail = pos

    def mix(self):
        for node in self.values:
            self.shift_node(node)

    def get_value(self, offset: int) -> int:
        node = self.zero
        for _ in range(offset):
            node = node.tail
        return node.value

    def get_coords(self) -> int:
        result = []
        for i in (1000, 2000, 3000):
            offset = i % self.size
            result.append(self.get_value(offset))
        return result

    def __str__(self) -> str:
        items = []
        for node in self.values:
            items.append(str(node.value))
        return ','.join(items)


def parse(stream) -> list:
    for line in stream:
        value = int(line.strip())
        yield value


def run(stream, test: bool = False):
    with timing("Part 1"):
        values = parse(stream)
        mixer = Mixer(values)
        mixer.mix()
        result1 = sum(mixer.get_coords())

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
