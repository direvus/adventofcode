"""Advent of Code 2017

Day 15: Duelling Generators

https://adventofcode.com/2017/day/15
"""
import logging  # noqa: F401

from util import timing, jit


DIVISOR = 2147483647
MATCH = 65535
FACTOR_A = 16807
FACTOR_B = 48271
MODULUS_A = 4
MODULUS_B = 8


class Generator:
    def __init__(self, initial: int, factor: int, modulus: int):
        self.initial = initial
        self.last = initial
        self.factor = factor
        self.modulus = modulus

    def reset(self):
        self.last = self.initial

    def next(self) -> int:
        value = (self.last * self.factor) % DIVISOR
        self.last = value
        return value

    def generate(self):
        value = self.next()
        while value % self.modulus != 0:
            value = self.next()
        return value


def get_generators(a: int, b: int) -> tuple[Generator]:
    """Return a pair of Generators, given their initial values."""
    return (
            Generator(a, FACTOR_A, MODULUS_A),
            Generator(b, FACTOR_B, MODULUS_B)
            )


def match16(a: int, b: int) -> bool:
    """Return whether two integers match in their lowest 16 bits."""
    return a & MATCH == b & MATCH


def parse(stream) -> tuple:
    result = []
    for line in stream:
        words = line.strip().split()
        result.append(int(words[-1]))
    return tuple(result)


@jit
def _count_matches(init_a: int, init_b: int, count: int) -> int:
    a = init_a
    b = init_b
    result = 0
    for i in range(count):
        a = (a * FACTOR_A) % DIVISOR
        b = (b * FACTOR_B) % DIVISOR
        result += int(a & MATCH == b & MATCH)
    return result


@jit
def _count_mod_matches(init_a: int, init_b: int, count: int) -> int:
    a = init_a
    b = init_b
    result = 0
    for i in range(count):
        a = (a * FACTOR_A) % DIVISOR
        while a % MODULUS_A:
            a = (a * FACTOR_A) % DIVISOR
        b = (b * FACTOR_B) % DIVISOR
        while b % MODULUS_B:
            b = (b * FACTOR_B) % DIVISOR
        result += int(a & MATCH == b & MATCH)
    return result


def count_matches(a: Generator, b: Generator, count: int) -> int:
    return _count_matches(a.initial, b.initial, count)


def count_mod_matches(a: Generator, b: Generator, count: int) -> int:
    return _count_mod_matches(a.initial, b.initial, count)


def run(stream, test: bool = False):
    with timing("Part 1"):
        init_a, init_b = parse(stream)
        a, b = get_generators(init_a, init_b)
        result1 = count_matches(a, b, 40 * 10 ** 6)

    with timing("Part 2"):
        a.reset()
        b.reset()
        result2 = count_mod_matches(a, b, 5 * 10 ** 6)

    return (result1, result2)
