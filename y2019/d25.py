"""Advent of Code 2019

Day 25: Cryostasis

https://adventofcode.com/2019/day/25
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


class Game:
    def __init__(self, stream):
        comp = Computer(stream)
        comp.set_input_hook(self.get_input)
        comp.set_output_hook(self.write_output)
        self.computer = comp
        self.inputs = []

    def get_input(self) -> int:
        if self.inputs:
            return self.inputs.pop(0)
        # Queue is empty, so prompt the user for more.
        text = input()
        self.inputs.extend(ord(x) for x in text)
        self.inputs.append(10)
        return self.inputs.pop(0)

    def write_output(self, outputs):
        text = ''.join(chr(x) for x in outputs)
        outputs.clear()
        print(text, end='')

    def play(self):
        self.computer.run()


def parse(stream) -> Game:
    return Game(stream)


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        game = parse(stream)
        game.play()
        result1 = 0

    result2 = 0

    return (result1, result2)
