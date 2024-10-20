"""Advent of Code 2020

Day 14: Docking Data

https://adventofcode.com/2020/day/14
"""
import logging  # noqa: F401
import re

from util import timing


class Computer:
    def __init__(self, stream=''):
        self.program = []
        self.memory = {}

        if stream:
            self.parse(stream)

    def parse_mask(self, mask: str) -> tuple[int, int]:
        pos = 0
        neg = 0
        for i, ch in enumerate(mask):
            if ch == '1':
                power = len(mask) - i - 1
                pos |= 1 << power
            elif ch == '0':
                power = len(mask) - i - 1
                neg |= 1 << power
        return pos, neg

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        pos = 0
        neg = 0
        for line in stream:
            line = line.strip()
            if line.startswith('mask = '):
                mask = line[7:]
                pos, neg = self.parse_mask(mask)
                continue
            m = re.fullmatch(r'^mem\[(\d+)\] = (\d+)$', line)
            if not m:
                continue
            addr = int(m.group(1))
            value = int(m.group(2))
            self.program.append((pos, neg, addr, value))

    def run(self):
        for pos, neg, addr, value in self.program:
            masked = (value | pos) & ~neg
            self.memory[addr] = masked


class ComputerV2(Computer):
    def parse_mask(self, mask: str) -> tuple[int, int]:
        pos = 0
        floated = 0
        for i, ch in enumerate(mask):
            if ch == '1':
                power = len(mask) - i - 1
                pos |= 1 << power
            elif ch == 'X':
                power = len(mask) - i - 1
                floated |= 1 << power
        return pos, floated

    def expand_mask(self, addr: int, floated: int) -> set[int]:
        result = {addr}
        for i in range(36):
            value = 1 << i
            if value > floated:
                break
            if not floated & value:
                continue
            new = set()
            for item in result:
                new.add(item & ~value)
                new.add(item | value)
            result |= new
        return result

    def run(self):
        for pos, floated, addr, value in self.program:
            masked = addr | pos
            for expanded in self.expand_mask(masked, floated):
                self.memory[expanded] = value


def parse(stream) -> Computer:
    return Computer(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        source = stream.read()
        comp = parse(source)
        comp.run()
        result1 = sum(comp.memory.values())

    with timing("Part 2"):
        if test:
            source = ("""
                    mask = 000000000000000000000000000000X1001X
                    mem[42] = 100
                    mask = 00000000000000000000000000000000X0XX
                    mem[26] = 1
                    """)
        comp = ComputerV2(source)
        comp.run()
        result2 = sum(comp.memory.values())

    return (result1, result2)
