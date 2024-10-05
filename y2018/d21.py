"""Advent of Code 2018

Day 21: Chronal Conversion

https://adventofcode.com/2018/day/21
"""
import logging  # noqa: F401

from util import timing


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
        while not self.halt:
            self.do_instruction()

    def to_string(self):
        code = self.program[self.pointer]
        registers = ' '.join([f'{x:5d}' for x in self.registers])
        return (
                f'{self.counter:5d} {self.pointer:2d} '
                f'{code[0]} {code[1]} {code[2]:2d} {code[3]} [{registers}]')

    def run_to_line(self, line: int):
        """Run the program until we arrive at a particular program line."""
        stop = False
        while not stop:
            self.do_instruction()
            stop = self.pointer == line

    def watch_line_register(self, line: int, register: int):
        while not self.halt:
            point = self.pointer
            self.do_instruction()
            new = self.registers[register]
            if point == line:
                print(new)

    def watch_registers(self, registers: set):
        while not self.halt:
            line = self.pointer
            count = self.counter
            self.do_instruction()
            inst = self.program[line]
            if inst[-1] in registers:
                new = self.registers[inst[-1]]
                logging.debug(
                        f"{count:6d} line {line:2d} "
                        f"{inst[0]} {inst[1]:d} {inst[2]:8d} {inst[3]:d} "
                        f"r{inst[-1]} -> {new}")


def rotate(x, y, scale: int):
    x += (y & 0xff)
    x = ((x & 0xffffff) * scale) & 0xffffff
    return x


def generate_series(start: int, scale: int):
    x = 0
    y = 0
    values = {}
    count = 0
    while True:
        y = x | 0x10000
        x = start
        x = rotate(x, y, scale)
        y = y // 0x100
        x = rotate(x, y, scale)
        y = y // 0x100
        x = rotate(x, y, scale)
        if x in values:
            logging.debug(f"{x} has been seen before")
            logging.debug(
                    f"{len(values)} values generated in "
                    f"{count + 1} iterations")
            break
        else:
            values[x] = count
        count += 1
    keys = list(values.keys())
    keys.sort(key=lambda x: values[x], reverse=True)
    return keys[0]


def run(stream, test: bool = False):
    if test:
        # There's no sample input for this puzzle, and really it's all about
        # inspecting an assembly program and figuring out how it works, so
        # there's no programming to speak of either.
        result1, result2 = (0, 0)
    else:
        with timing("Part 1"):
            comp = Computer()
            comp.parse(stream)
            result1 = 0

        with timing("Part 2"):
            result2 = generate_series(6152285, 65899)

    return (result1, result2)
