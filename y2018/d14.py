"""Advent of Code 2018

Day 14: Chocolate Charts

https://adventofcode.com/2018/day/14
"""
import logging  # noqa: F401

from util import timing, get_digits


class Node:
    """A node of a singly-linked (forward) list."""
    def __init__(self, value: int, nex: 'Node' = None):
        self.value = value
        self.nex = nex


class Board:
    def __init__(self, scores: tuple, positions: tuple):
        self.workers = []
        self.count = 0
        self.scores = None
        for i, score in enumerate(scores):
            node = self.append(score)
            if i in positions:
                self.workers.append(node)

    def append(self, score: int) -> Node:
        node = Node(score)
        if self.scores is None:
            # Create a new singly-linked list that loops back to itself.
            node.nex = node
        else:
            # Append to the end of the existing list
            prev = self.scores
            node.nex = prev.nex
            prev.nex = node
        self.scores = node
        self.count += 1
        return node

    def move(self, node: Node, count: int) -> Node:
        """Move forward through the list from `node`, `count` times."""
        result = node
        for _ in range(count):
            result = result.nex
        return result

    def update(self) -> int:
        """Run one round of creating new scores.

        Each worker reads the score from their node, we sum those scores
        together, and create a new node from each digit of the sum. The new
        nodes are appended to the end of the score list, and the workers each
        move forward through the list one plus their current score times.

        Return the number of scores added.
        """
        total = sum(n.value for n in self.workers)
        digits = get_digits(total)
        result = len(digits)
        for digit in digits:
            self.append(digit)

        for i, node in enumerate(self.workers):
            count = node.value + 1
            self.workers[i] = self.move(node, count)
        return result

    def to_string(self) -> str:
        if self.scores is None:
            return 'None'
        start = self.scores.nex
        node = start
        result = []
        workers = {id(x) for x in self.workers}
        while not result or node is not start:
            if id(node) in workers:
                result.append(f'[{node.value}]')
            else:
                result.append(f' {node.value} ')
            node = node.nex
        return ''.join(result)

    def get_scores(self, start: int, count: int) -> tuple:
        """Return the next `count` recipes after `start`.

        Continue to update the board until we have `start` recipes, then
        generate `count` more and return their values.
        """
        while self.count < start:
            self.update()
        # Grab a pointer to the current end node. Each update can generate one
        # or two scores, so we might have overshot the target. If so, take the
        # current end node as the first score of our result.
        result = []
        node = self.scores
        if self.count > start:
            result.append(node)

        while self.count < start + count:
            self.update()

        while len(result) < count:
            node = node.nex
            result.append(node.value)
        return result

    def is_next_equal(self, node: Node, digits: tuple) -> bool:
        """Return whether the next scores after `node` match `digits`."""
        for i, digit in enumerate(digits):
            node = node.nex
            if digit != node.value:
                return False
        return True

    def get_count_before(self, target: int | str) -> int:
        """Return the number of recipes before the digits in `target`.

        Continue to update the board until a sequence of scores matching the
        digits in `targets` appears, then return the number of recipes on the
        board before that sequence.
        """
        if isinstance(target, int):
            digits = get_digits(target)
        else:
            digits = tuple(int(x) for x in target)
        # Maintain a pointer that lags behind the end of the score board by the
        # length of our target sequence, and a count of the number of scores up
        # to that pointer
        reader = self.scores
        counter = self.count
        diff = 0
        while True:
            diff += self.update()
            while diff > len(digits):
                reader = self.move(reader, 1)
                diff -= 1
                counter += 1
                # Now see if the target sequence appears
                if self.is_next_equal(reader, digits):
                    return counter


def parse(stream) -> int:
    return int(stream.readline().strip())


def run(stream, test: bool = False):
    with timing("Part 1"):
        count = parse(stream)
        board = Board((3, 7), (0, 1))
        scores = board.get_scores(count, 10)
        result1 = ''.join(str(x) for x in scores)

    with timing("Part 2"):
        target = 92510 if test else count
        board = Board((3, 7), (0, 1))
        result2 = board.get_count_before(target)

    return (result1, result2)
