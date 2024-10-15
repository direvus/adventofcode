"""Advent of Code 2019

Day 22: _TITLE_

https://adventofcode.com/2019/day/22
"""
import logging  # noqa: F401

from util import timing


class Shuffle:
    def __init__(self, size: int, program: str = ''):
        self.size = size
        self.cards = list(range(size))
        self.program = []
        self.parse(program)

    def reset(self):
        self.cards = list(range(self.size))

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

    def run(self):
        for fn, args in self.program:
            fn(*args)

    def find_cycle(self, index: int) -> int:
        history = {}
        i = 0
        while True:
            self.run()
            card = self.cards[index]
            logging.info(
                    f"{i}: card at {index} is {card}")
            if card in history:
                logging.info(
                        f"    card {card} was last seen at {history[card]}")
            history[card] = i
            i += 1


def run(stream, test: bool = False):
    with timing("Part 1"):
        size = 10 if test else 10007
        shuffle = Shuffle(size)
        shuffle.parse(stream)
        shuffle.run()

        if test:
            result1 = ' '.join(str(x) for x in shuffle.cards)
        else:
            result1 = shuffle.cards.index(2019)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
