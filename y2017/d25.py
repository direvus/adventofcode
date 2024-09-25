"""Advent of Code 2017

Day 25: The Halting Problem

https://adventofcode.com/2017/day/25
"""
import logging  # noqa: F401
from collections import defaultdict, namedtuple

from util import timing


State = namedtuple('state', ['name', 'actions'])
Action = namedtuple('action', ['write', 'move', 'next'])


class TuringMachine:
    def __init__(self):
        self.tape = defaultdict(lambda: 0)
        self.pointer = 0
        self.counter = 0
        self.state = None
        self.states = {}
        self.steps = 0

    @property
    def current(self):
        return self.tape[self.pointer]

    def parse(self, stream) -> tuple:
        line = stream.readline().strip().strip('.')
        self.state = line.split()[-1]

        line = stream.readline().strip().strip('.')
        self.steps = int(line.split()[-2])

        line = stream.readline()
        while line:
            line = line.strip()
            if line == '':
                line = stream.readline().strip()

            line = line.strip(':')
            name = line.split()[-1]
            actions = []

            for _ in range(2):
                stream.readline()
                line = stream.readline().strip().strip('.')
                write = int(line.split()[-1])

                line = stream.readline().strip().strip('.')
                move = 1 if line.split()[-1] == 'right' else -1

                line = stream.readline().strip().strip('.')
                nxt = line.split()[-1]

                a = Action(write, move, nxt)
                actions.append(a)
            state = State(name, actions)
            self.states[name] = state
            line = stream.readline()

        stream.readline()
        line = stream.readline()

    def run_step(self):
        state = self.states[self.state]
        action = state.actions[self.current]
        self.tape[self.pointer] = action.write
        self.pointer += action.move
        self.state = action.next

    def run(self) -> int:
        for _ in range(self.steps):
            self.run_step()
        return sum(self.tape.values())


def run(stream, test: bool = False):
    with timing("Part 1"):
        tm = TuringMachine()
        tm.parse(stream)
        logging.debug(vars(tm))
        result1 = tm.run()

    result2 = 0
    return (result1, result2)
