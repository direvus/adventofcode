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
    def __init__(self, source: list[int]):
        self.maximum = 0
        self.current = None
        self.values = {}

        prev = None
        for value in source:
            self.maximum = max(value, self.maximum)
            node = Node(value)
            if prev is None:
                self.current = node
            else:
                prev.tail = node
            self.values[value] = node
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
        return self.values[value]

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

        node = self.get_node(dest)
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

    def get_next_values(self, target: int, count: int):
        result = []
        node = self.get_node(target)
        for _ in range(count):
            node = node.tail
            result.append(node.value)
        return result


def parse(stream) -> list[int]:
    result = []
    for ch in stream.readline().strip():
        result.append(int(ch))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        source = parse(stream)
        game = Game(source)
        game.do_rounds(100)
        result1 = game.get_order()

    with timing("Part 2"):
        maximum = max(source)
        if test:
            count = 1000
            rounds = 10_000
        else:
            count = 1_000_000
            rounds = 10_000_000
        for n in range(maximum + 1, count + 1):
            source.append(n)
        game = Game(source)
        game.do_rounds(rounds)
        a, b = game.get_next_values(1, 2)
        result2 = a * b

    return (result1, result2)
