"""Advent of Code 2022

Day 11: Monkey in the Middle

https://adventofcode.com/2022/day/11
"""
import logging  # noqa: F401
from collections import deque
from operator import add, mul

from util import timing


class Monkey:
    def __init__(self):
        self.items = deque()
        self.operation = None
        self.operand = None
        self.divisor = None
        self.true_target = None
        self.false_target = None
        self.counter = 0

    def parse(self, stream):
        # Starting items
        line = stream.readline().strip()
        itemlist = line.split(': ')[1]
        for item in itemlist.split(', '):
            self.items.append(int(item))

        # Operation
        line = stream.readline().strip()
        expr = line.split('= old ')[1]
        symbol, operand = expr.split()
        match symbol:
            case '+':
                self.operation = add
            case '*':
                self.operation = mul
            case _:
                raise ValueError(f'Unknown symbol {symbol}')
        if operand == 'old':
            self.operand = 'old'
        else:
            self.operand = int(operand)

        # Test
        line = stream.readline().strip()
        self.divisor = int(line.split(' divisible by ')[1])

        # If true
        line = stream.readline().strip()
        self.true_target = int(line.split()[-1])

        # If false
        line = stream.readline().strip()
        self.false_target = int(line.split()[-1])

    def throw_items(self):
        while self.items:
            item = self.items.popleft()
            operand = item if self.operand == 'old' else self.operand
            item = self.operation(item, operand) // 3
            divisible = item % self.divisor == 0
            target = self.true_target if divisible else self.false_target
            self.counter += 1
            yield (target, item)


def parse(stream) -> list:
    result = []
    for line in stream:
        if line.startswith('Monkey'):
            monkey = Monkey()
            monkey.parse(stream)
            result.append(monkey)
    return result


def do_round(monkeys: list):
    for monkey in monkeys:
        for target, item in monkey.throw_items():
            monkeys[target].items.append(item)


def get_inspection_counts(monkeys: list, count: int = 20):
    for i in range(count):
        do_round(monkeys)
    return [m.counter for m in monkeys]


def run(stream, test: bool = False):
    with timing("Part 1"):
        monkeys = parse(stream)
        counts = get_inspection_counts(monkeys)
        counts.sort(reverse=True)
        result1 = counts[0] * counts[1]

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
