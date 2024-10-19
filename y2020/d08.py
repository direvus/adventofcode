"""Advent of Code 2020

Day 8: Handheld Halting

https://adventofcode.com/2020/day/8
"""
import logging  # noqa: F401

from util import timing


class Computer:
    def __init__(self, stream: str = ''):
        self.program = []
        self.memory = []
        self.halt = False
        self.pointer = 0
        self.acc = 0

        self.instructions = {
                'acc': self.do_accumulate,
                'jmp': self.do_jump,
                'nop': self.do_nothing,
                }
        if stream:
            self.parse(stream)

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        program = []
        for line in stream:
            line = line.strip()
            if line == '':
                continue
            code, arg = line.split()
            arg = int(arg)
            program.append((code, arg))
        self.program = tuple(program)
        self.load_program()

    def load_program(self):
        self.memory.clear()
        self.memory = list(self.program)

    def reset(self):
        self.load_program()
        self.pointer = 0
        self.acc = 0
        self.halt = False

    def do_accumulate(self, arg: int):
        self.acc += arg
        self.pointer += 1

    def do_jump(self, arg: int):
        self.pointer += arg

    def do_nothing(self, arg: int):
        self.pointer += 1

    def do_instruction(self):
        if self.pointer == len(self.memory):
            self.halt = True
            return
        code, arg = self.memory[self.pointer]
        if code not in self.instructions:
            raise ValueError(f"Unknown opcode {code} at {self.pointer}")
        self.instructions[code](arg)

    def run_until_loop(self):
        history = set()
        while not (self.halt or self.pointer in history):
            history.add(self.pointer)
            self.do_instruction()


def parse(stream) -> Computer:
    return Computer(stream)


def find_corrupt_instruction(comp: Computer) -> int:
    """Locate the corrupt instruction in the program.

    For each 'jmp' or 'nop' instruction in the program, try flipping it to the
    other instruction without changing its argument. Then run the program,
    stopping if any loop is encountered.

    Return the value of the accumulator after the first time a program
    successfully runs and halts without encountering any loops.
    """
    for i in range(len(comp.program)):
        code, arg = comp.memory[i]
        if code not in {'jmp', 'nop'}:
            continue
        comp.reset()
        newcode = 'jmp' if code == 'nop' else 'nop'
        comp.memory[i] = (newcode, arg)
        comp.run_until_loop()
        if comp.halt:
            # Exited normally
            return comp.acc


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        comp.run_until_loop()
        result1 = comp.acc

    with timing("Part 2"):
        result2 = find_corrupt_instruction(comp)

    return (result1, result2)
