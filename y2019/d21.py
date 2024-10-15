"""Advent of Code 2019

Day 21: Springdroid Adventure

https://adventofcode.com/2019/day/21
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


class Droid:
    def __init__(self, intcode_program):
        self.computer = Computer(intcode_program)
        self.program = ''

    def reset(self):
        self.computer.reset()

    def add_inputs(self, inputs: str):
        self.computer.add_inputs(ord(x) for x in inputs)

    def load_program(self, program: str):
        self.program = program

    def execute(self, run: bool = False) -> int:
        self.add_inputs(self.program)
        command = 'RUN\n' if run else 'WALK\n'
        self.add_inputs(command)
        outputs = []
        for output in self.computer.generate():
            if output > 255:
                return output
            outputs.append(chr(output))
        logging.error(''.join(outputs))

    def walk(self) -> int:
        return self.execute(False)

    def run(self) -> int:
        return self.execute(True)


def parse(stream) -> Droid:
    return Droid(stream)


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        droid = parse(stream)
        droid.load_program(
                'NOT A J\n'
                'NOT B T\n'
                'OR T J\n'
                'NOT C T\n'
                'OR T J\n'
                'AND D J\n')
        result1 = droid.walk()

    with timing("Part 2"):
        droid.reset()
        droid.load_program(
                'OR A J\n'
                'AND B J\n'
                'AND C J\n'
                'NOT J J\n'
                'OR E T\n'
                'OR H T\n'
                'AND T J\n'
                'AND D J\n')
        result2 = droid.run()

    return (result1, result2)
