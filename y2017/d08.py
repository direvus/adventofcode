"""Advent of Code 2017

Day 8: I Heard You Like Registers

https://adventofcode.com/2017/day/8
"""
import logging  # noqa: F401
from collections import defaultdict, namedtuple

from util import timing


Instruction = namedtuple(
        'instruction',
        ('target', 'amount', 'check', 'operator', 'value'))


class Computer:
    def __init__(self):
        self.counter = 0
        self.pointer = 0
        self.registers = defaultdict(lambda: 0)
        self.program = []

    def reset(self):
        self.counter = 0
        self.pointer = 0
        self.registers.clear()

    def parse_program(self, stream) -> tuple:
        self.program = []
        for line in stream:
            line = line.strip()
            words = line.split(' ')
            target = words[0]
            amount = int(words[2])
            if words[1] == 'dec':
                amount = -amount
            check, op, value = words[4:]
            value = int(value)
            inst = Instruction(target, amount, check, op, value)
            self.program.append(inst)
        return self.program

    def do_instruction(self, instruction) -> None:
        """Execute one instruction on the Computer."""
        value = self.registers[instruction.check]
        cond = False
        match instruction.operator:
            case '==':
                cond = value == instruction.value
            case '!=':
                cond = value != instruction.value
            case '<':
                cond = value < instruction.value
            case '>':
                cond = value > instruction.value
            case '<=':
                cond = value <= instruction.value
            case '>=':
                cond = value >= instruction.value
        if cond:
            self.registers[instruction.target] += instruction.amount

    def run_program(self) -> int:
        """Run the current program until the Computer halts.

        Each instruction will give a target register, an amount to add to that
        register, and a criterion. The criterion is a register name, an
        operator and a comparison value. If the criterion is met, we adjust the
        target register, otherwise we do nothing.

        When all instructions have been executed once, the program halts.

        Return the highest value held in any register during the run.
        """
        self.pointer = 0
        result = float('-inf')
        while self.pointer < len(self.program):
            inst = self.program[self.pointer]
            self.do_instruction(inst)
            self.pointer += 1
            result = max(result, self.get_largest_value())
        return result

    def get_largest_value(self) -> int:
        return max(self.registers.values())


def run(stream, test: bool = False):
    with timing("Parsing"):
        comp = Computer()
        comp.parse_program(stream)

    with timing("Parts 1 + 2"):
        result2 = comp.run_program()
        result1 = comp.get_largest_value()

    return (result1, result2)
