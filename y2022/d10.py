"""Advent of Code 2022

Day 10: Cathode-Ray Tube

https://adventofcode.com/2022/day/10
"""
import logging  # noqa: F401

from util import timing


class Computer:
    def __init__(self):
        self.counter = 0
        self.pointer = 0
        self.clock = 0
        self.register = 1
        self.program = []
        self.update_hook = None

    def update_clock(self):
        self.clock += 1
        if self.update_hook:
            self.update_hook(self.clock, self.register)

    def do_noop(self):
        self.update_clock()

    def do_addx(self, value: int):
        self.update_clock()
        self.update_clock()
        self.register += value

    def do_instruction(self):
        instruction = self.program[self.pointer]
        self.pointer += 1
        match instruction[0]:
            case 'addx':
                self.do_addx(int(instruction[1]))
            case 'noop':
                self.do_noop()

    def run(self):
        self.clock = 0
        self.pointer = 0
        self.register = 1
        while self.pointer < len(self.program):
            self.do_instruction()

    def find_signals(self) -> list[int]:
        signals = []

        def add_signal(tick, value):
            if tick in {20, 60, 100, 140, 180, 220}:
                signals.append(tick * value)
        self.update_hook = add_signal
        self.run()
        return signals

    def render_screen(self) -> str:
        pixels = []

        def draw_pixel(tick, value):
            pos = (tick - 1) % 40
            char = '#' if abs(value - pos) <= 1 else '.'
            pixels.append(char)
        self.update_hook = draw_pixel
        self.run()
        logging.debug(pixels)

        rows = []
        for i in range(0, len(pixels), 40):
            rows.append(''.join(pixels[i: i + 40]))
        return '\n'.join(rows)


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        words = line.split()
        result.append(words)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        program = parse(stream)
        computer = Computer()
        computer.program = tuple(program)
        signals = computer.find_signals()
        result1 = sum(signals)

    with timing("Part 2"):
        output = computer.render_screen()
        result2 = output

    return (result1, result2)
