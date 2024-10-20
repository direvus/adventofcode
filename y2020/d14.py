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
                pos |= 2 ** power
            elif ch == '0':
                power = len(mask) - i - 1
                neg |= 2 ** power
        return pos, neg

    def parse(self, stream):
        pos = 0
        neg = 0
        for line in stream:
            line = line.strip()
            if line.startswith('mask = '):
                mask = line[7:]
                pos, neg = self.parse_mask(mask)
                continue
            m = re.fullmatch(r'^mem\[(\d+)\] = (\d+)$', line)
            addr = int(m.group(1))
            value = int(m.group(2))
            self.program.append((pos, neg, addr, value))

    def run(self):
        for pos, neg, addr, value in self.program:
            masked = (value | pos) & ~neg
            self.memory[addr] = masked


def parse(stream) -> Computer:
    return Computer(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = parse(stream)
        comp.run()
        result1 = sum(comp.memory.values())

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
