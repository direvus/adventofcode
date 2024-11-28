"""Advent of Code 2022

Day 20: Grove Positioning System

https://adventofcode.com/2022/day/20
"""
import logging  # noqa: F401

from util import timing


KEY = 811589153


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
        steps = node.value % (self.size - 1)
        if steps == 0:
            return

        head = node.head
        tail = node.tail

        # remove the node from its current position
        head.tail = tail
        tail.head = head

        pos = tail
        for _ in range(steps):
            pos = pos.tail

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
        node = self.zero
        items.append(str(node.value))
        while node.tail != self.zero:
            node = node.tail
            items.append(str(node.value))
        return ','.join(items)


def parse(stream) -> list:
    result = []
    for line in stream:
        value = int(line.strip())
        result.append(value)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        values = parse(stream)
        mixer = Mixer(values)
        mixer.mix()
        result1 = sum(mixer.get_coords())

    with timing("Part 2"):
        values2 = map(lambda x: x * KEY, values)
        mixer2 = Mixer(values2)
        for _ in range(10):
            mixer2.mix()
        result2 = sum(mixer2.get_coords())

    return (result1, result2)
