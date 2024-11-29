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

    def wrap(self, position: tuple, facing: int) -> tuple:
        px, py = position
        if facing % 2 == 0:
            # Horizontal facing
            values = {x for x, y in self.cells if y == py}
            px = min(values) if facing == 0 else max(values)
        else:
            # Vertical facing
            values = {y for x, y in self.cells if x == px}
            py = min(values) if facing == 1 else max(values)
        return (px, py), facing

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
            f = facing
            if n not in self.cells:
                # Wrap around to the other side of the map.
                n, f = self.wrap(position, facing)
            if n in self.walls:
                # Hit a wall, stop here.
                return position, facing
            if n in self.spaces:
                # Move into the space and keep going.
                position = n
                facing = f
                i += 1
        return position, facing

    def get_final_position(self, instructions: tuple) -> tuple:
        position = self.start
        facing = 0

        for instruction in instructions:
            position, facing = self.do_instruction(
                    position, facing, instruction)

        return (position, facing)


class CubeGrid(Grid):
    def __init__(self, facesize: int, wrappings: tuple, mappings: dict):
        super().__init__()
        self.facesize = facesize
        self.wrappings = wrappings
        self.mappings = mappings
        self.reverse_mapping = {v: k for k, v in mappings.items()}

    def copy_from(self, other: Grid):
        self.spaces = other.spaces
        self.walls = other.walls
        self.cells = other.cells
        self.start = other.start

    def get_region(self, position: tuple) -> int:
        x = position[0] // self.facesize
        y = position[1] // self.facesize
        return self.mappings.get((x, y), None)

    def get_corner_offset(self, position: tuple, facing: int) -> int:
        x, y = position
        value = x if facing % 2 else y
        return value % self.facesize

    def get_face_position(self, position: tuple) -> tuple:
        x, y = position
        return (x % self.facesize, y % self.facesize)

    def wrap_face_position(
            self, facepos: tuple, facing: int, rotation: int) -> tuple:
        x, y = facepos
        maximum = self.facesize - 1
        if facing % 2:
            # Vertical
            y = maximum if y == 0 else 0
        else:
            # Horizontal
            x = maximum if x == 0 else 0

        if rotation == 0:
            return x, y
        elif rotation == 1:
            return maximum - y, x
        elif rotation == 2:
            return maximum - x, maximum - y
        elif rotation == 3:
            return y, maximum - x

    def wrap(self, position: tuple, facing: int) -> tuple:
        px, py = position
        region = self.get_region(position)
        offset = self.get_corner_offset(position, facing)
        logging.debug(f'{position} is in region {region} with offset {offset}')
        r, f = self.wrappings[region][facing]
        logging.debug(f'wraps to {r} facing {FACING[f]}')

        facepos = self.get_face_position(position)
        rotation = (f - facing) % 4
        x, y = self.wrap_face_position(facepos, facing, rotation)
        rx, ry = self.reverse_mapping[r]
        logging.debug(f'target region at {(rx, ry)}')
        x += rx * self.facesize
        y += ry * self.facesize
        logging.debug(f'final location {(x, y)}')
        return (x, y), f


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
        # In theory we could analyse the shape of the grid, figure out which of
        # the 11 possible cube nets it is, and build up the wrappings from
        # that, but I can't be bothered with that right now. Instead I will
        # hard-code the wrappings and region mappings for the test input and my
        # actual input.
        if test:
            size = 4
            mappings = {
                    (2, 0): 0,
                    (2, 1): 1,
                    (3, 2): 2,
                    (1, 1): 3,
                    (0, 1): 4,
                    (2, 2): 5,
                    }
            wrappings = (
                    ((2, 2), (1, 1), (3, 1), (4, 1)),
                    ((2, 1), (5, 1), (3, 2), (0, 3)),
                    ((0, 2), (4, 0), (5, 2), (1, 2)),
                    ((1, 0), (5, 0), (4, 2), (0, 0)),
                    ((3, 0), (5, 3), (2, 3), (0, 1)),
                    ((2, 0), (4, 3), (3, 3), (1, 3)),
                    )
        else:
            size = 50
            mappings = {
                    (1, 0): 0,
                    (1, 1): 1,
                    (2, 0): 2,
                    (0, 2): 3,
                    (0, 3): 4,
                    (1, 2): 5,
                    }
            wrappings = (
                    ((2, 0), (1, 1), (3, 0), (4, 0)),
                    ((2, 3), (5, 1), (3, 1), (0, 3)),
                    ((5, 2), (1, 2), (0, 2), (4, 3)),
                    ((5, 0), (4, 1), (0, 0), (1, 0)),
                    ((5, 3), (2, 1), (0, 1), (3, 3)),
                    ((2, 2), (4, 2), (3, 2), (1, 3)),
                    )
        cube = CubeGrid(size, wrappings, mappings)
        cube.copy_from(grid)
        (x, y), f = cube.get_final_position(instructions)
        result2 = get_password(y + 1, x + 1, f)

    return (result1, result2)
