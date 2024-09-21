"""Advent of Code 2016

Day 25: Clock Signal

https://adventofcode.com/2016/day/25
"""
import logging  # noqa: F401

from util import timing


class Computer:
    def __init__(self):
        self.counter = 0
        self.pointer = 0
        self.registers = {k: 0 for k in {'a', 'b', 'c', 'd'}}
        self.program = []

    def reset(self):
        self.counter = 0
        self.pointer = 0
        self.registers = {k: 0 for k in {'a', 'b', 'c', 'd'}}

    def parse_program(self, stream) -> list:
        self.program = []
        for line in stream:
            line = line.strip()
            words = line.split(' ')
            inst = words[0]
            operands = words[1:]
            self.program.append((inst, operands))
        return self.program

    def get_value(self, value: str) -> int:
        """Get the value for a split-type operand.

        The value can either be an integer literal, or a reference to a
        register. If it's an integer literal, return that value as an integer.
        If it's a register reference, return the value held in that register.
        """
        if value in self.registers:
            return self.registers[value]
        return int(value)

    def toggle_instruction(self, index: int):
        if index < 0 or index >= len(self.program):
            return
        inst, ops = self.program[index]
        numops = len(ops)
        if numops == 1:
            inst = 'dec' if inst == 'inc' else 'inc'
        elif numops == 2:
            inst = 'cpy' if inst == 'jnz' else 'jnz'
        self.program[index] = (inst, ops)

    def do_instruction(self, instruction, operands) -> int:
        """Execute one instruction on the Computer.

        Return the offset to the next instruction, relative to the current one.
        """
        # It's a feature of this particular instruction set that each
        # instruction has a unique first letter, so that's all we need to
        # compare.
        match instruction[0]:
            case 'c':
                src, dest = operands
                value = self.get_value(src)
                if dest in self.registers:
                    # If this instruction refers to an invalid register (e.g.
                    # by being toggled by a `tgl` instruction, skip it.
                    self.registers[dest] = value
            case 'i':
                self.registers[operands[0]] += 1
            case 'd':
                self.registers[operands[0]] -= 1
            case 'j':
                testval = self.get_value(operands[0])
                if testval != 0:
                    return self.get_value(operands[1])
            case 't':
                offset = self.get_value(operands[0])
                self.toggle_instruction(self.pointer + offset)
        return 1

    def run_program(self):
        """Run the current program until the Computer halts.

        Each instruction will supply an offset to the next instruction to
        execute. The Computer halts when that offset points outside of the
        program space.

        When the `out` instruction is executed, this method yields the value of
        the operand, so it can be used as a generator function for programs
        that produce an output signal.
        """
        self.pointer = 0
        self.counter = 0
        while self.pointer >= 0 and self.pointer < len(self.program):
            inst, ops = self.program[self.pointer]
            offset = self.do_instruction(inst, ops)

            if inst == 'out':
                yield self.get_value(ops[0])

            self.counter += 1
            if self.pointer == 27:
                logging.debug(
                        f"{self.counter:4d} {self.pointer:4d} "
                        f"{inst} \\[{', '.join(ops):6s}] {offset} -> "
                        f"{self.registers['a']:4d} {self.registers['b']:4d} "
                        f"{self.registers['c']:4d} {self.registers['d']:4d}")
            self.pointer += offset


def get_sequence(start):
    result = []
    value = start
    while value > 0:
        result.append(value % 2)
        value //= 2
    return result


def run(stream, test: bool = False):
    comp = Computer()
    comp.parse_program(stream)

    with timing("Part 1"):
        start = 2534
        result1 = start
        while True:
            seq = get_sequence(result1)
            if seq == [i % 2 for i in range(len(seq))]:
                break
            result1 += 4
        result1 -= start

    return (result1, None)