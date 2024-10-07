"""Advent of Code 2019

Day 2: 1202 Program Alarm

https://adventofcode.com/2019/day/2
"""
import logging  # noqa: F401

from util import timing


class Computer:
    def __init__(self):
        self.program = []
        self.memory = []
        self.pointer = 0
        self.halt = False

    def parse(self, stream):
        line = stream.readline().strip()
        self.program = tuple(int(x) for x in line.split(','))
        self.memory = list(self.program)

    def reset(self):
        self.memory = list(self.program)
        self.pointer = 0
        self.halt = False

    def do_instruction(self):
        i = self.pointer
        opcode = self.memory[i]
        if opcode == 99:
            self.halt = True
            return
        if opcode == 1:
            a = self.memory[i + 1]
            b = self.memory[i + 2]
            c = self.memory[i + 3]
            result = self.memory[a] + self.memory[b]
            self.memory[c] = result
            self.pointer += 4
            return
        if opcode == 2:
            a = self.memory[i + 1]
            b = self.memory[i + 2]
            c = self.memory[i + 3]
            result = self.memory[a] * self.memory[b]
            self.memory[c] = result
            self.pointer += 4
            return
        raise ValueError(f"{opcode} is not a valid opcode")

    def run(self):
        while not self.halt:
            self.do_instruction()

    def find_inputs(self, target: int) -> tuple:
        for a in range(100):
            for b in range(100):
                self.reset()
                self.memory[1] = a
                self.memory[2] = b
                self.run()
                result = self.memory[0]
                if result == target:
                    return a, b


def parse(stream) -> Computer:
    comp = Computer()
    comp.parse(stream)
    return comp


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        if test:
            comp.run()
        else:
            comp.memory[1] = 12
            comp.memory[2] = 2
            comp.run()
        result1 = comp.memory[0]

    with timing("Part 2"):
        if test:
            result2 = 0
        else:
            target = 19690720
            noun, verb = comp.find_inputs(target)
            result2 = noun * 100 + verb

    return (result1, result2)
