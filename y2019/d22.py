"""Advent of Code 2019

Day 22: Slam Shuffle

https://adventofcode.com/2019/day/22
"""
import logging  # noqa: F401

from util import timing


def compose(f: tuple, g: tuple, m: int) -> tuple:
    """Compose two linear congruential functions.

    The arguments `f` and `g` should be each be tuples of two integers,
    representing the coefficients of a linear congruential function, where both
    functions have the modulus `m`.

    That is, if the function f(x) is of the form:

        f(x) = (Ax + B) mod m

    Then the tuple argument for `f` should be (A, B).

    The result is a tuple representing the coefficients of the composed
    function, all modulo `m`.
    """
    return ((f[0] * g[0]) % m, (f[1] * g[0] + g[1]) % m)


def pow_compose(f: tuple, n: int, m: int) -> tuple:
    """Compose a linear congruential function into itself.

    The function is composed into itself `n` times, using an exponentiation by
    squaring trick.
    """
    g = (1, 0)
    while n > 0:
        if n % 2:
            g = compose(g, f, m)
        n //= 2
        f = compose(f, f, m)
    return g


def pow_mod(x: int, n: int, m: int) -> int:
    """Raise `x` to the power `n`, modolu `m`."""
    y = 1
    while n > 0:
        if n % 2:
            y = (y * x) % m
        n //= 2
        x = (x * x) % m
    return y


def invert(x: int, m: int) -> int:
    """Return the modular inverse of `x` modulo `m`.

    This function will only work with values of `m` that are prime.
    """
    return pow_mod(x, m - 2, m) % m


class Shuffle:
    def __init__(self, size: int, program: str = ''):
        self.size = size
        self.program = []
        self.lcf = None
        self.parse(program)

    def parse(self, program: str):
        if isinstance(program, str):
            program = program.split('\n')

        self.program = []
        for line in program:
            line = line.strip()
            if line == '':
                continue
            words = line.split()
            if words[0] == 'cut':
                fn = self.cut
                args = (int(words[1]),)
            elif words[0:2] == ['deal', 'into']:
                fn = self.reverse
                args = tuple()
            elif words[0:2] == ['deal', 'with']:
                fn = self.inc
                args = (int(words[-1]),)
            else:
                raise ValueError(f"Unrecognised instruction {line}")

            self.program.append((fn, args))

    def reverse(self):
        self.cards.reverse()

    def cut(self, index: int):
        self.cards = self.cards[index:] + self.cards[:index]

    def inc(self, increment: int):
        arr = [None] * self.size
        index = 0
        count = 0
        while count < self.size:
            card = self.cards[count]
            arr[index] = card
            count += 1
            index = (index + increment) % self.size
        self.cards = arr

    def setup_deck(self):
        self.cards = list(range(self.size))

    def run(self):
        for fn, args in self.program:
            fn(*args)

    def get_lcf(self) -> tuple:
        """Return an LCF tuple for the operations in this shuffle."""
        if self.lcf is not None:
            return self.lcf

        result = (1, 0)
        for fn, args in self.program:
            if fn == self.reverse:
                f = (-1, -1)
            elif fn == self.cut:
                f = (1, -args[0])
            elif fn == self.inc:
                f = (args[0], 0)
            result = compose(result, f, self.size)
        self.lcf = result
        return result

    def find_position(self, card: int) -> int:
        """Return the final position of `card` after one complete shuffle."""
        a, b = self.get_lcf()
        return (a * card + b) % self.size

    def find_index(self, index: int, repeats: int) -> int:
        """Return the card at `index` after `repeats` complete shuffles."""
        f = self.get_lcf()
        a, b = pow_compose(f, repeats, self.size)
        inverse_a = invert(a, self.size)
        return ((index - b) * inverse_a) % self.size


def run(stream, test: bool = False):
    with timing("Part 1"):
        size = 10 if test else 10007
        shuffle = Shuffle(size)
        shuffle.parse(stream)

        if test:
            shuffle.setup_deck()
            shuffle.run()
            result1 = ' '.join(str(x) for x in shuffle.cards)
        else:
            result1 = shuffle.find_position(2019)

    with timing("Part 2"):
        if test:
            # There's no test case for this insanity
            result2 = 0
        else:
            shuffle.size = 119315717514047
            shuffle.lcf = None  # Force the LCF to be recalculated
            result2 = shuffle.find_index(2020, 101741582076661)

    return (result1, result2)
