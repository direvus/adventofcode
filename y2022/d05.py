"""Advent of Code 2022

Day 5: Supply Stacks

https://adventofcode.com/2022/day/5
"""
import logging  # noqa: F401
from collections import deque
from copy import deepcopy

from util import timing


class Stacks:
    def __init__(self):
        self.stacks = []

    def add_crate(self, stack: int, crate: str):
        while len(self.stacks) <= stack:
            self.stacks.append(deque())
        self.stacks[stack].append(crate)

    def move_crates(self, count: int, source: int, dest: int):
        for i in range(count):
            self.stacks[dest].appendleft(self.stacks[source].popleft())

    def do_moves(self, moves):
        for count, source, dest in moves:
            self.move_crates(count, source, dest)

    def get_top_crates(self):
        return (stack[0] for stack in self.stacks)


class Stacks2(Stacks):
    def move_crates(self, count: int, source: int, dest: int):
        temp = []
        for i in range(count):
            temp.append(self.stacks[source].popleft())
        while temp:
            self.stacks[dest].appendleft(temp.pop())


def parse(stream) -> Stacks:
    stacks = Stacks()
    for line in stream:
        if line[1].isdigit():
            break
        for i in range(1, len(line), 4):
            if line[i].isupper():
                stacks.add_crate((i - 1) // 4, line[i])
    # discard one blank line
    stream.readline()
    moves = []
    for line in stream:
        line = line.strip()
        words = line.split()
        moves.append((int(words[1]), int(words[3]) - 1, int(words[5]) - 1))
    return stacks, moves


def run(stream, test: bool = False):
    with timing("Part 1"):
        stacks, moves = parse(stream)
        stacks2 = Stacks2()
        stacks2.stacks = deepcopy(stacks.stacks)
        stacks.do_moves(moves)
        result1 = ''.join(stacks.get_top_crates())

    with timing("Part 2"):
        stacks2.do_moves(moves)
        result2 = ''.join(stacks2.get_top_crates())

    return (result1, result2)
