"""Advent of Code 2022

Day 22: Monkey Map

https://adventofcode.com/2022/day/22
"""
import logging  # noqa: F401
import re

from util import timing


FACING = ('>', 'v', '<', '^')
VECTORS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def get_password(row: int, column: int, facing: int) -> int:
    return (row * 1000) + (column * 4) + facing


def move(position: tuple, facing: int, count: int = 1) -> tuple:
    x, y = position
    vx, vy = VECTORS[facing]
    return (x + vx * count, y + vy * count)


def turn(facing: int, rotation: int):
    return (facing + rotation) % 4


class Grid:
    def __init__(self):
        self.start = None
        self.walls = set()
        self.spaces = set()
        self.cells = set()

    def parse(self, stream):
        y = 0
        for line in stream:
            if line.strip() == '':
                break
            for x, ch in enumerate(line):
                if ch == '#':
                    self.walls.add((x, y))
                elif ch == '.':
                    self.spaces.add((x, y))
                    if self.start is None:
                        self.start = (x, y)
            y += 1
        self.cells = self.spaces | self.walls

    def get_wrapped_cell(self, position: tuple, facing: int) -> tuple:
        px, py = position
        if facing % 2 == 0:
            # Horizontal facing
            values = {x for x, y in self.cells if y == py}
            px = min(values) if facing == 0 else max(values)
        else:
            # Vertical facing
            values = {y for x, y in self.cells if x == px}
            py = min(values) if facing == 1 else max(values)
        return px, py

    def do_instruction(
            self, position: tuple, facing: int,
            instruction: str | int) -> tuple:
        if instruction in {'L', 'R'}:
            rotation = 1 if instruction == 'R' else -1
            facing = turn(facing, rotation)
            return position, facing

        i = 0
        while i < instruction:
            n = move(position, facing, 1)
            if n not in self.cells:
                # Wrap around to the other side of the map.
                n = self.get_wrapped_cell(position, facing)
            if n in self.walls:
                # Hit a wall, stop here.
                return position, facing
            if n in self.spaces:
                # Move into the space and keep going.
                position = n
                i += 1
        return position, facing

    def get_final_position(self, instructions: tuple) -> tuple:
        position = self.start
        facing = 0

        for instruction in instructions:
            position, facing = self.do_instruction(
                    position, facing, instruction)

        return (position, facing)


def parse(stream) -> tuple:
    grid = Grid()
    grid.parse(stream)

    # The grid parser will have consumed the blank line
    line = stream.readline().strip()
    instructions = []
    for part in re.split(r'([LR])', line):
        if part.isdigit():
            instructions.append(int(part))
        else:
            instructions.append(part)

    return (grid, instructions)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid, instructions = parse(stream)
        (x, y), f = grid.get_final_position(instructions)
        result1 = get_password(y + 1, x + 1, f)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
