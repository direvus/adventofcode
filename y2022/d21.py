"""Advent of Code 2022

Day 21: Monkey Math

https://adventofcode.com/2022/day/21
"""
import logging  # noqa: F401
from collections import namedtuple
from operator import add, sub, mul, floordiv

from util import timing


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        monkey, op = line.split(': ')
        result.append((monkey, op.split()))
    return result


Node = namedtuple('Node', ('name', 'value', 'left', 'operator', 'right'))


class Graph:
    def __init__(self):
        self.nodes = {}

    def load(self, monkeys):
        for monkey, words in monkeys:
            if len(words) == 1:
                node = Node(monkey, int(words[0]), None, None, None)
            else:
                match words[1]:
                    case '+':
                        op = add
                    case '-':
                        op = sub
                    case '*':
                        op = mul
                    case '/':
                        op = floordiv
                node = Node(monkey, None, words[0], op, words[2])
            self.nodes[monkey] = node

    def evaluate(self, monkey: str) -> int:
        node = self.nodes[monkey]
        if node.value is not None:
            return node.value

        a = self.evaluate(node.left)
        b = self.evaluate(node.right)
        return node.operator(a, b)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        graph = Graph()
        graph.load(parsed)
        result1 = graph.evaluate('root')

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
