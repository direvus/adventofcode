"""Advent of Code 2019

Day 14: Space Stoichiometry

https://adventofcode.com/2019/day/14
"""
import logging  # noqa: F401
from collections import defaultdict
from math import ceil

from util import timing


class Reaction:
    def __init__(self, output: str, quantity: int, inputs: dict):
        self.output = output
        self.quantity = quantity
        self.inputs = inputs


class Graph:
    def __init__(self, stream=None):
        self.nodes = set()
        self.reactions = {}
        if stream:
            self.parse(stream)

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        for line in stream:
            line = line.strip()
            if line == '':
                continue
            left, right = line.split(' => ')
            inputs = {}
            for item in left.split(', '):
                count, name = item.split(' ')
                inputs[name] = int(count)
            count, output = right.split(' ')
            reaction = Reaction(output, int(count), inputs)
            self.reactions[output] = reaction

    def find_ore_required(self, product: str, count: int = 1) -> int:
        """Find the way to produce `product` for the least ore.

        Return the smallest amount of ore required to produce `count` units of
        `product`.
        """
        assert count > 0
        if product == 'ORE':
            return count

        q = [(product, count)]
        stock = defaultdict(lambda: 0)
        ore = 0

        while q:
            p, c = q.pop(0)

            if p == 'ORE':
                ore += c
                continue

            if stock[p] > 0:
                amount = min(c, stock[p])
                stock[p] -= amount
                c -= amount
                if c <= 0:
                    continue

            reaction = self.reactions[p]
            repeats = ceil(c / reaction.quantity)
            produced = repeats * reaction.quantity
            stock[p] += produced - c

            for inp, qty in reaction.inputs.items():
                qty *= repeats
                q.append((inp, qty))
        return ore

    def get_fuel(self, ore: int) -> int:
        """Return the amount of fuel that can be produced with `ore`."""

        # Use a bisecting search to find the highest fuel value that does not
        # exceed the allowed ore amount.
        low = ore // self.find_ore_required('FUEL', 1)
        high = low * 2
        diff = high - low

        while diff > 0:
            req = self.find_ore_required('FUEL', high)
            diff = (high - low) // 2
            if req == ore:
                return high
            if req > ore:
                high -= diff
            else:
                low = high
                high += diff
        return low


def parse(stream) -> Graph:
    return Graph(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        graph = parse(stream)
        result1 = graph.find_ore_required('FUEL')

    with timing("Part 2"):
        result2 = graph.get_fuel(10 ** 12)

    return (result1, result2)
