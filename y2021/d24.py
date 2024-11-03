"""Advent of Code 2021

Day 24: Arithmetic Logic Unit

https://adventofcode.com/2021/day/24
"""
import logging  # noqa: F401
from collections import deque

from util import timing


REGISTERS = 'wxyz'


class Computer:
    def __init__(self):
        self.pointer = 0
        self.counter = 0
        self.registers = [0, 0, 0, 0]
        self.program = []
        self.inputs = deque()

    def load_program(self, program):
        for inst, operands in program:
            self.program.append((inst, operands))

    def reset(self):
        self.pointer = 0
        self.counter = 0
        self.registers = [0, 0, 0, 0]
        self.inputs.clear()

    def add_input(self, value):
        self.inputs.append(value)

    def get_value(self, value):
        if value in REGISTERS:
            return self.registers[REGISTERS.index(value)]
        else:
            return int(value)

    def write_value(self, register, value):
        self.registers[REGISTERS.index(register)] = value

    def do_inp(self, register: str):
        value = self.inputs.popleft()
        self.write_value(register, value)

    def do_add(self, register, value):
        value = self.get_value(value)
        self.registers[REGISTERS.index(register)] += value

    def do_mul(self, register, value):
        value = self.get_value(value)
        self.registers[REGISTERS.index(register)] *= value

    def do_div(self, register, value):
        value = self.get_value(value)
        self.registers[REGISTERS.index(register)] //= value

    def do_mod(self, register, value):
        value = self.get_value(value)
        self.registers[REGISTERS.index(register)] %= value

    def do_eql(self, register, value):
        a = self.get_value(register)
        b = self.get_value(value)
        self.write_value(register, int(a == b))

    def do_instruction(self):
        inst, ops = self.program[self.pointer]
        match inst:
            case 'inp':
                self.do_inp(ops[0])
                return
            case 'add':
                self.do_add(*ops)
                return
            case 'mul':
                self.do_mul(*ops)
                return
            case 'div':
                self.do_div(*ops)
                return
            case 'mod':
                self.do_mod(*ops)
                return
            case 'eql':
                self.do_eql(*ops)
                return

    def to_pseudocode(self):
        inst, ops = self.program[self.pointer]
        match inst:
            case 'inp':
                return f'{ops[0]} = input'
            case 'add':
                return f'{ops[0]} += {ops[1]}'
            case 'mul':
                return f'{ops[0]} *= {ops[1]}'
            case 'div':
                return f'{ops[0]} //= {ops[1]}'
            case 'mod':
                return f'{ops[0]} %= {ops[1]}'
            case 'eql':
                return f'{ops[0]} = 1 if ({ops[0]} == {ops[1]}) else 0'

    def execute(self):
        self.pointer = 0
        self.counter = 0
        while self.pointer < len(self.program):
            self.do_instruction()
            inst, ops = self.program[self.pointer]
            self.pointer += 1
            self.counter += 1


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        words = line.split()
        result.append((words[0], words[1:]))
    return result


def validate_number(computer, number: int) -> bool:
    digits = str(number)
    if '0' in digits:
        return False
    for digit in digits:
        computer.add_input(int(digit))
    computer.execute()
    return computer.registers[3] == 0


def run(stream, test: bool = False):
    with timing("Part 1"):
        program = parse(stream)
        comp = Computer()
        comp.load_program(program)
        if test:
            comp.add_input(7)
            comp.execute()
            result1 = comp.registers
        else:
            comp.reset()
            # There's no sensible way to write a solver for this, it was just a
            # matter of reading the code and figuring out what it meant.
            #
            # The constraints on a valid number are:
            # - the first digit must be 4 less than the last digit
            # - the second digit must be 8 less than the thirteenth digit (so
            # the second must be 1 and the thirteenth must be 9)
            # - the third digit must be 6 more than the sixth digit
            # - the fourth digit must be 6 less than the fifth
            # - the seventh digit must be 2 more than the eighth
            # - the ninth digit must be 1 more than the tenth
            # - the eleventh digit must be the same as the twelfth
            result1 = 51_939_397_989_999
            assert validate_number(comp, result1)

    with timing("Part 2"):
        if test:
            result2 = 0
        else:
            result2 = 11_717_131_211_195
            comp.reset()
            assert validate_number(comp, result2)

    return (result1, result2)
