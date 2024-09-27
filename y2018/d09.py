"""Advent of Code 2018

Day 9: Marble Mania

https://adventofcode.com/2018/day/9
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing


class Node:
    """A node in a continuous doubly-linked list."""
    def __init__(self, value, pre=None, nex=None):
        self.value = value
        self.pre = pre
        self.nex = nex


class Game:
    def __init__(self):
        self.players = 0
        self.last = 0
        self.turn = 0
        self.current = None
        self.scores = defaultdict(lambda: 0)

    def parse(self, stream):
        line = stream.readline().strip()
        words = line.split()
        self.players = int(words[0])
        self.last = int(words[-2])

    def move(self, node: Node, count: int) -> Node:
        """Return the node `count` steps clockwise from `node`."""
        for _ in range(abs(count)):
            node = node.nex if count > 0 else node.pre
        return node

    def insert(self, node: Node, value: int) -> Node:
        """Insert a new node before `node`."""
        pre = node.pre
        new = Node(value, pre, node)
        pre.nex = new
        node.pre = new
        return new

    def remove(self, node: Node) -> int:
        """Remove a node and return its value."""
        pre = node.pre
        nex = node.nex
        pre.nex = nex
        nex.pre = pre
        return node.value

    def do_turn(self, marble: int):
        if marble % 23 == 0:
            # Scoring marble
            player = self.turn % self.players
            self.scores[player] += marble

            node = self.move(self.current, -7)
            self.current = node.nex
            self.scores[player] += node.value
            self.remove(node)
            return
        # Normal marble
        node = self.move(self.current, 2)
        self.current = self.insert(node, marble)

    def get_nodes_string(self) -> str:
        result = [str(self.current.value)]
        node = self.current
        while node.nex != self.current:
            node = node.nex
            result.append(str(node.value))
        return ' '.join(result)

    def play(self):
        self.current = Node(0)
        self.current.pre = self.current
        self.current.nex = self.current
        self.turn = 1
        marble = 1

        while marble <= self.last:
            self.do_turn(marble)
            self.turn += 1
            marble += 1

    def get_win_score(self):
        return max(self.scores.values())


def run(stream, test: bool = False):
    with timing("Part 1"):
        game1 = Game()
        game1.parse(stream)
        game1.play()
        result1 = game1.get_win_score()

    with timing("Part 2"):
        game2 = Game()
        game2.players = game1.players
        game2.last = game1.last * 100
        game2.play()
        result2 = game2.get_win_score()

    return (result1, result2)
