"""Advent of Code 2017

Day 10: Knot Hash

https://adventofcode.com/2017/day/10
"""
import logging  # noqa: F401
from functools import reduce
from operator import xor

from util import timing


MAGIC_SUFFIX = (17, 31, 73, 47, 23)


def parse(stream) -> tuple:
    line = stream.readline().strip()
    values = tuple(int(x.strip()) for x in line.split(','))
    return values, line


def reduce_xor(values) -> int:
    return reduce(xor, values)


class Knot:
    def __init__(self, size: int):
        self.size = size
        self.items = list(range(size))
        self.position = 0
        self.skip = 0

    def twist(self, length):
        assert length <= self.size
        start = self.position
        end = start + length
        if end > self.size:
            end = end % self.size
            sublist = self.items[start:] + self.items[:end]
            remain = self.items[end:start]
            sublist = list(reversed(sublist))
            split = self.size - start
            self.items = sublist[split:] + remain + sublist[:split]
        else:
            self.items = (
                    self.items[:start] +
                    list(reversed(self.items[start:end])) +
                    self.items[end:])
        self.position = (self.position + length + self.skip) % self.size
        self.skip += 1

    def do_round(self, lengths) -> int:
        for length in lengths:
            self.twist(length)
            logging.debug(self.items)
        return self.items[0] * self.items[1]

    def get_dense_hash(self, value: str, rounds: int = 64) -> tuple[int]:
        """Calculate the dense hash of an input string.

        Return the hash values as a tuple of 16 integers.
        """
        codes = tuple(ord(c) for c in value) + MAGIC_SUFFIX
        for _ in range(rounds):
            self.do_round(codes)

        result = tuple(
                reduce_xor(self.items[i:i + 16])
                for i in range(0, self.size, 16))
        return result


def get_hash(value: str) -> str:
    """Return the Knot Hash of value as a hexadecimal string."""
    k = Knot(256)
    v = k.get_dense_hash(value)
    return ''.join(f'{x:02x}' for x in v)


def run(stream, test: bool = False):
    input1, input2 = parse(stream)

    with timing("Part 1"):
        size = 5 if test else 256
        knot = Knot(size)
        result1 = knot.do_round(input1)

    with timing("Part 2"):
        result2 = get_hash(input2)

    return (result1, result2)
