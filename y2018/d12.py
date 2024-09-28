"""Advent of Code 2018

Day 12: Subterranean Sustainability

https://adventofcode.com/2018/day/12
"""
import logging  # noqa: F401

from util import timing


class Farm:
    def __init__(self):
        self.plants = set()
        self.rules = set()

    def parse(self, stream):
        header = stream.readline().strip()
        state = header.split()[-1]
        self.plants = {i for i, x in enumerate(state) if x == '#'}
        # skip one blank line
        stream.readline()
        for line in stream:
            pattern, result = line.strip().split(' => ')
            # Don't bother ingesting rules that don't produce a plant
            if result != '#':
                continue
            self.rules.add(tuple(int(ch == '#') for ch in pattern))

    @property
    def sum(self):
        return sum(self.plants)

    def update(self):
        """Process one generation of plant growth."""
        left = min(self.plants) - 4
        right = max(self.plants) + 5
        state = tuple(int(i in self.plants) for i in range(left, right))
        new = set()
        for i in range(len(state) - 5):
            c = left + i + 2
            if state[i:i + 5] in self.rules:
                new.add(c)
        self.plants = new

    def run(self, count: int = 1):
        """Run `count` generations of updates."""
        for i in range(count):
            self.update()


def run(stream, test: bool = False):
    with timing("Part 1"):
        farm = Farm()
        farm.parse(stream)
        farm.run(20)
        result1 = farm.sum

    with timing("Part 2"):
        farm.run(79)
        # After a hundred generations, both the test and actual inputs have
        # settled into stable linear patterns, so we can extrapolate out for
        # any future generation number.
        total1 = farm.sum
        farm.update()
        total2 = farm.sum
        diff = total2 - total1
        logging.debug(f"Sum is increasing by {diff} per generation")
        result2 = total2 + diff * (50_000_000_000 - 100)

    return (result1, result2)
