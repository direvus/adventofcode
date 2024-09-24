"""Advent of Code 2017

Day 23: Coprocessor Conflagration

https://adventofcode.com/2017/day/23
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import timing, is_prime


def parse_program(stream) -> tuple:
    program = []
    for line in stream:
        line = line.strip()
        words = line.split(' ')
        program.append((words[0], words[1:]))
    return program


class Computer:
    def __init__(self, name: str = ''):
        self.name = name
        self.counter = 0
        self.pointer = 0
        self.registers = defaultdict(lambda: 0)
        self.program = []

    def reset(self):
        self.counter = 0
        self.pointer = 0
        self.registers.clear()

    def get_value(self, value: str) -> int:
        """Get the value for a split-type operand.

        The value can either be an integer literal, or a reference to a
        register. If it's an integer literal, return that value as an integer.
        If it's a register reference, return the value held in that register.
        """
        if value in string.ascii_lowercase:
            return self.registers[value]
        return int(value)

    def parse(self, stream) -> tuple:
        self.program = parse_program(stream)
        return self.program

    def do_instruction(self, instruction, operands) -> None:
        """Execute one instruction on the Computer.

        Modifies the Computer's instruction pointer directly.
        """
        offset = 1
        match instruction:
            case 'set':
                reg, value = operands
                self.registers[reg] = self.get_value(value)
            case 'sub':
                reg, value = operands
                self.registers[reg] -= self.get_value(value)
            case 'mul':
                reg, value = operands
                self.registers[reg] *= self.get_value(value)
            case 'jnz':
                testval = self.get_value(operands[0])
                if testval != 0:
                    offset = self.get_value(operands[1])
        self.pointer += offset

    def run_program(self, watch: str = None) -> int:
        """Run the current program until the Computer halts.

        Each do_instruction() call will modify the instruction pointer.  The
        Computer halts when that pointer points outside of the program space.

        If a `watch` value is provided, count the number of times that
        instruction is invoked.
        """
        self.pointer = 0
        self.counter = 0
        result = 0
        length = len(self.program)
        while self.pointer >= 0 and self.pointer < length:
            index = self.pointer
            inst, ops = self.program[index]
            self.do_instruction(inst, ops)
            self.counter += 1

            if watch == inst:
                result += 1
            logging.debug(
                    f"{self.name} {self.counter:4d} {index:4d} "
                    f"{inst} \\[{', '.join(ops):6s}] -> "
                    f"{dict(self.registers)}")
        return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp1 = Computer()
        comp1.parse(stream)
        result1 = comp1.run_program('mul')

    with timing("Part 2"):
        comp2 = Computer()
        comp2.program = comp1.program
        comp2.registers['a'] = 1
        # Don't run the actual program, just count the number of primes from
        # 108400 to 125400 stepping up by 17.
        result2 = 0
        for n in range(108_400, 125_401, 17):
            if not is_prime(n):
                result2 += 1

    return (result1, result2)
