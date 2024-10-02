"""Advent of Code 2018

Day 19: Go With The Flow

https://adventofcode.com/2018/day/19
"""
import logging  # noqa: F401

from util import timing, get_divisors


class Computer:
    def __init__(self):
        self.pointer = 0
        self.counter = 0
        self.bind = 0
        self.registers = [0 for _ in range(6)]
        self.program = []
        self.halt = False

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            words = line.split()
            if line.startswith('#ip'):
                self.bind = int(words[1])
                continue

            opcode = words[0]
            operands = tuple(int(x) for x in words[1:])
            self.program.append((opcode,) + operands)

    def reset(self):
        self.pointer = 0
        self.counter = 0
        self.registers = [0 for _ in range(6)]
        self.halt = False

    def do_instruction(self):
        """Perform the next instruction."""
        self.registers[self.bind] = self.pointer
        words = self.program[self.pointer]
        opcode = words[0]
        a, b, c = words[1:]
        match opcode:
            case 'addr':
                self.registers[c] = self.registers[a] + self.registers[b]
            case 'addi':
                self.registers[c] = self.registers[a] + b
            case 'mulr':
                self.registers[c] = self.registers[a] * self.registers[b]
            case 'muli':
                self.registers[c] = self.registers[a] * b
            case 'banr':
                self.registers[c] = self.registers[a] & self.registers[b]
            case 'bani':
                self.registers[c] = self.registers[a] & b
            case 'borr':
                self.registers[c] = self.registers[a] | self.registers[b]
            case 'bori':
                self.registers[c] = self.registers[a] | b
            case 'setr':
                self.registers[c] = self.registers[a]
            case 'seti':
                self.registers[c] = a
            case 'gtir':
                self.registers[c] = int(a > self.registers[b])
            case 'gtri':
                self.registers[c] = int(self.registers[a] > b)
            case 'gtrr':
                self.registers[c] = int(self.registers[a] > self.registers[b])
            case 'eqir':
                self.registers[c] = int(a == self.registers[b])
            case 'eqri':
                self.registers[c] = int(self.registers[a] == b)
            case 'eqrr':
                self.registers[c] = int(self.registers[a] == self.registers[b])
        self.pointer = self.registers[self.bind]
        self.pointer += 1
        self.counter += 1
        if self.pointer < 0 or self.pointer >= len(self.program):
            self.halt = True

    def run(self):
        """Run the program until the computer halts."""
        logging.debug(self.to_string())
        while not self.halt:
            self.do_instruction()

    def to_string(self):
        code = self.program[self.pointer]
        registers = ' '.join([f'{x:5d}' for x in self.registers])
        return (
                f'{self.counter:5d} {self.pointer:2d} '
                f'{code[0]} {code[1]} {code[2]:2d} {code[3]} [{registers}]')


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = Computer()
        comp.parse(stream)
        comp.run()
        result1 = comp.registers[0]

    with timing("Part 2"):
        if test:
            comp.reset()
            comp.registers[0] = 1
            comp.run()
            result2 = comp.registers[0]
        else:
            # There's no point trying to run Part 2 on the actual input
            result2 = sum(get_divisors(10551358))

    return (result1, result2)
