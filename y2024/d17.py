"""Advent of Code 2024

Day 17: Chronospatial Computer

https://adventofcode.com/2024/day/17
"""
import logging  # noqa: F401
from collections import deque

import assembly
from util import timing, jit


class Computer(assembly.Computer):
    def __init__(self, registers):
        instructions = [
                self.do_adv,
                self.do_bxl,
                self.do_bst,
                self.do_jnz,
                self.do_bxc,
                self.do_out,
                self.do_bdv,
                self.do_cdv,
                ]

        super().__init__(list(registers), instructions)
        self.outputs = []

    def get_combo_value(self, value: int):
        if value < 4:
            return value
        if value < 7:
            return self.registers[value - 4]
        raise ValueError(f'invalid operand combo value {value}')

    def do_adv(self, operand):
        denom = 2 ** self.get_combo_value(operand)
        self.registers[0] //= denom

    def do_bxl(self, operand):
        self.registers[1] = self.registers[1] ^ operand

    def do_bst(self, operand):
        self.registers[1] = self.get_combo_value(operand) % 8

    def do_jnz(self, operand):
        if self.registers[0] == 0:
            return None
        self.pointer = operand
        return 0

    def do_bxc(self, operand):
        self.registers[1] ^= self.registers[2]

    def do_out(self, operand):
        self.outputs.append(self.get_combo_value(operand) % 8)

    def do_bdv(self, operand):
        denom = 2 ** self.get_combo_value(operand)
        self.registers[1] = self.registers[0] // denom

    def do_cdv(self, operand):
        denom = 2 ** self.get_combo_value(operand)
        self.registers[2] = self.registers[0] // denom

    def do_instruction(self):
        """Execute the instruction at the current instruction pointer.

        Afterwards, the instruction pointer will be advanced by the return
        value of the instruction call, or else by 2 if the call does not return
        a value.

        In any case, return the result of the instruction.
        """
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer + 1]
        fn = self.instructions[opcode]
        result = fn(operand)

        if result is None:
            self.pointer += 2
        else:
            self.pointer += result
        self.counter += 1

        return result


def parse(stream) -> list:
    registers = tuple(
            int(stream.readline().strip().split(': ')[1])
            for _ in range(3))
    stream.readline()
    text = stream.readline().strip().split(': ')[1]
    program = tuple(map(int, text.split(',')))
    return registers, program


@jit
def get_output(a, test):
    if test:
        return (a // 8) % 8

    b = (a % 8) ^ 2
    c = (a // (2 ** b))
    return ((b ^ 7) ^ c) % 8


def get_outputs(initial):
    a = initial
    while a != 0:
        yield get_output(a)
        a //= 8


def find_copy_values(program, test):
    q = deque()
    q.append((0, len(program) - 1))
    result = set()
    while q:
        start, index = q.popleft()
        for value in range(start, start + 8):
            if get_output(value, test) == program[index]:
                if index == 0:
                    result.add(value)
                else:
                    q.append((value * 8, index - 1))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        registers, program = parse(stream)
        computer = Computer(registers)
        computer.load_program(program)
        computer.run()
        result1 = ','.join(map(str, computer.outputs))

    with timing("Part 2"):
        if test:
            program = (0, 3, 5, 4, 3, 0)
        result2 = min(find_copy_values(program, test))

    return (result1, result2)
