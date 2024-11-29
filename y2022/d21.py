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
        self.parent = {}

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
                left = words[0]
                right = words[2]
                node = Node(monkey, None, left, op, right)
                self.parent[left] = monkey
                self.parent[right] = monkey
            self.nodes[monkey] = node

    def evaluate(self, monkey: str) -> int:
        node = self.nodes[monkey]
        if node.value is not None:
            return node.value

        a = self.evaluate(node.left)
        b = self.evaluate(node.right)
        return node.operator(a, b)

    def get_path(self, start: str) -> tuple:
        result = [start]
        node = start
        while node in self.parent:
            node = self.parent[node]
            result.append(node)
        return tuple(result)

    def get_target(self) -> int:
        """Return the number needed at 'humn' to balance 'root'.

        The return value will be the number that, if it were returned from the
        'humn' node, would result in both branches of the 'root' node having
        the same value.
        """
        path = self.get_path('humn')
        branch = path[-2]

        # Evaluate the branch that doesn't include 'humn'.
        root = self.nodes['root']
        other = root.left if root.right == branch else root.right
        target = self.evaluate(other)

        # Now walk back down towards 'humn', figuring out what value is
        # required at each step.
        for i in reversed(range(1, len(path) - 1)):
            node = self.nodes[path[i]]
            left = node.left == path[i - 1]
            fixed = node.right if left else node.left
            other = self.evaluate(fixed)

            if node.operator is add:
                target -= other
            elif node.operator is mul:
                target //= other
            elif node.operator is sub:
                if left:
                    target += other
                else:
                    target = -target + other
            elif node.operator is floordiv:
                if left:
                    target *= other
                else:
                    target = other // target
        return target


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        graph = Graph()
        graph.load(parsed)
        result1 = graph.evaluate('root')

    with timing("Part 2"):
        result2 = graph.get_target()

    return (result1, result2)
