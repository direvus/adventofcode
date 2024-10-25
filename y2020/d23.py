"""Advent of Code 2020

Day 23: Crab Cups

https://adventofcode.com/2020/day/23
"""
import logging  # noqa: F401

from util import timing


class Node:
    """A node of a singly-linked (forward) list."""
    def __init__(self, value: int, tail: 'Node' = None):
        self.value = value
        self.tail = tail


class Game:
    def __init__(self, source: str):
        self.maximum = 0
        self.current = None

        prev = None
        for char in source:
            value = int(char)
            self.maximum = max(value, self.maximum)
            node = Node(value)
            if prev is None:
                self.current = node
            else:
                prev.tail = node
            prev = node
        prev.tail = self.current

    def __str__(self) -> str:
        line = []
        node = self.current
        while node.tail != self.current:
            line.append(str(node.value))
            node = node.tail
        line.append(str(node.value))
        return ' '.join(line)

    def get_node(self, value: int) -> Node:
        node = self.current
        while node.value != value:
            node = node.tail
        return node

    def do_round(self):
        node = self.current
        head = self.current.tail
        collected = set()
        for _ in range(3):
            node = node.tail
            collected.add(node.value)
        node = node.tail
        self.current.tail = node

        dest = self.current.value - 1
        if dest < 1:
            dest = self.maximum
        while dest in collected:
            dest = dest - 1 if dest > 1 else self.maximum

        while node.value != dest:
            node = node.tail

        tail = node.tail
        node.tail = head
        head.tail.tail.tail = tail
        self.current = self.current.tail

    def do_rounds(self, count: int = 1):
        for i in range(count):
            self.do_round()

    def get_order(self) -> str:
        node = self.get_node(1).tail
        line = []
        while node.value != 1:
            line.append(str(node.value))
            node = node.tail
        return ''.join(line)


def parse(stream) -> Game:
    return Game(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = parse(stream)
        game.do_rounds(100)
        result1 = game.get_order()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
