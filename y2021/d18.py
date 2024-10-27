"""Advent of Code 2021

Day 18: Snailfish

https://adventofcode.com/2021/day/18
"""
import logging  # noqa: F401
from itertools import permutations
from math import ceil, floor

from util import timing


class Number:
    def __init__(self, stream=''):
        self.values = []
        if stream:
            self.parse(stream)

    def parse(self, line: str):
        i = 0
        depth = 0
        while i < len(line):
            ch = line[i]
            if ch == '[':
                depth += 1
                i += 1
                continue
            elif ch == ']':
                depth -= 1
                i += 1
                continue
            elif ch.isdigit():
                digits = [ch]
                i += 1
                while line[i].isdigit():
                    digits.append(line[i])
                    i += 1
                value = int(''.join(digits))
                self.values.append([depth, value])
                continue
            else:
                i += 1

    def add(self, other):
        result = Number()
        values = self.values + other.values
        result.values = [[d + 1, v] for d, v in values]
        result.reduce()
        return result

    def __add__(self, other):
        return self.add(other)

    def do_reduce_round(self) -> bool:
        """Perform one round of reduction.

        Return a boolean to indicate whether we performed any action (explode
        or split) in this round.
        """
        # First, check for exploding pairs -- anything with depth greater than
        # 4.
        for i in range(len(self.values) - 1):
            depth, value = self.values[i]
            if depth > 4:
                # Add the left value leftwards, if possible
                if i > 0:
                    self.values[i - 1][1] += value
                # Add the right value rightwards, if possible
                if i < len(self.values) - 2:
                    value = self.values[i + 1][1]
                    self.values[i + 2][1] += value
                # Replace this entire pair with a zero at one higher depth
                # level. This is modifying a list while we are traversing it,
                # but we are about to exit the function so that's fine.
                self.values[i: i + 2] = [[depth - 1, 0]]
                return True

        # Since nothing exploded, move on to checking for splits. The first
        # number we encounter that is 10 or greater will be split.
        for i in range(len(self.values)):
            depth, value = self.values[i]
            if value > 9:
                left = floor(value / 2)
                right = ceil(value / 2)
                depth += 1
                self.values[i: i + 1] = [[depth, left], [depth, right]]
                return True

        return False

    def reduce(self):
        """Perform reduce rounds until no action occurs."""
        action = True
        while action:
            action = self.do_reduce_round()

    @property
    def magnitude(self):
        """Pop, pop!"""
        values = list(self.values)
        while len(values) > 1:
            # Look for two consecutive values at the same depth
            for i in range(len(values) - 1):
                if values[i][0] == values[i + 1][0]:
                    left = values[i][1]
                    right = values[i + 1][1]
                    magnitude = left * 3 + right * 2
                    values[i: i + 2] = [[values[i][0] - 1, magnitude]]
                    break
        return values[0][1]


def parse(stream) -> list[Number]:
    result = []
    for line in stream:
        line = line.strip()
        number = Number(line)
        result.append(number)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        numbers = parse(stream)
        total = numbers[0]
        for number in numbers[1:]:
            total += number
        result1 = total.magnitude

    with timing("Part 2"):
        result2 = 0
        for perm in permutations(numbers, 2):
            a, b = perm
            total = a + b
            magnitude = total.magnitude
            if magnitude > result2:
                result2 = magnitude

    return (result1, result2)
