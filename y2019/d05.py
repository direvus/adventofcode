"""Advent of Code 2019

Day 5: Sunny with a Chance of Asteroids

https://adventofcode.com/2019/day/5
"""
import logging  # noqa: F401

from util import timing


class Computer:
    def __init__(self):
        self.program = []
        self.memory = []
        self.pointer = 0
        self.halt = False
        self.inputs = []
        self.outputs = []

        self.instructions = {
                99: self.do_halt,
                1: self.do_add,
                2: self.do_mul,
                3: self.do_input,
                4: self.do_output,
                }

    def parse(self, stream):
        line = stream.readline().strip()
        self.program = tuple(int(x) for x in line.split(','))
        self.memory = list(self.program)

    def reset(self):
        self.memory = list(self.program)
        self.pointer = 0
        self.halt = False

    def get_value(self, modes: int, index: int):
        pos = self.memory[self.pointer + index]
        modes = str(modes)
        try:
            mode = modes[-index]
        except IndexError:
            mode = '0'
        match mode:
            case '0':
                return self.memory[pos]
            case '1':
                return pos
        raise ValueError(f"Unknown parameter mode {mode}")

    def do_halt(self, modes: int):
        self.halt = True

    def do_add(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        c = self.memory[self.pointer + 3]
        result = a + b
        self.memory[c] = result
        self.pointer += 4

    def do_mul(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        c = self.memory[self.pointer + 3]
        result = a * b
        self.memory[c] = result
        self.pointer += 4

    def do_input(self, modes: int):
        a = self.memory[self.pointer + 1]
        v = self.inputs.pop(0)
        self.memory[a] = v
        logging.debug(f"Got input {v} and stored it at {a}")
        self.pointer += 2

    def do_output(self, modes: int):
        v = self.get_value(modes, 1)
        self.outputs.append(v)
        self.pointer += 2

    def do_instruction(self):
        value = self.memory[self.pointer]
        modes, opcode = divmod(value, 100)
        if opcode not in self.instructions:
            raise ValueError(f"Unknown opcode {opcode} at {self.pointer}")
        self.instructions[opcode](modes)

    def run(self, inputs: tuple[int]) -> tuple[int]:
        self.inputs = list(inputs)
        while not self.halt:
            self.do_instruction()
        return tuple(self.outputs)


def parse(stream) -> Computer:
    comp = Computer()
    comp.parse(stream)
    return comp


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        outputs = comp.run([1])
        result1 = outputs[-1]

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
