"""Advent of Code 2019

Day 17: Set and Forget

https://adventofcode.com/2019/day/17
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Grid:
    def __init__(self, stream=None):
        self.scaffolds = set()
        self.position = (0, 0)
        self.direction = 0
        self.computer = Computer()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        self.computer.parse(stream)

    def reset(self):
        self.computer.reset()

    def get_neighbours(self, position: tuple) -> set:
        adjacent = {move(position, d) for d in range(len(DIRECTIONS))}
        return adjacent & self.scaffolds

    def get_intersections(self) -> set:
        result = set()
        for p in self.scaffolds:
            if len(self.get_neighbours(p)) > 2:
                result.add(p)
        return result

    def get_total_alignments(self) -> int:
        total = 0
        for p in self.get_intersections():
            total += p[0] * p[1]
        return total

    def get_camera_view(self) -> str:
        result = []
        y = 0
        x = 0
        for code in self.computer.generate():
            ch = chr(code)
            if ch == '\n':
                y += 1
                x = 0
                result.append(ch)
                continue
            elif ch == '#':
                self.scaffolds.add((x, y))
            elif ch in DIRECTIONS:
                self.direction = DIRECTIONS.index(ch)
                self.position = (x, y)
                self.scaffolds.add((x, y))
            result.append(ch)
            x += 1
        return ''.join(result)

    def format_inputs(self, inputs):
        """Format inputs for the program.

        Elements from inputs are delimited by comma and terminated by newline,
        and the entire string is then returned as a tuple of integer ASCII
        character codes.
        """
        line = ','.join(str(x) for x in inputs) + '\n'
        return tuple(ord(x) for x in line)

    def add_inputs(self, inputs):
        self.computer.add_inputs(self.format_inputs(inputs))

    def run(self) -> int:
        """Walk the robot through the entire scaffold.

        Return the final output value from the program.
        """
        self.reset()
        self.computer.memory[0] = 2
        moves_a = ('R', 6, 'L', 6, 'L', 10)
        moves_b = ('L', 8, 'L', 6, 'L', 10, 'L', 6)
        moves_c = ('R', 6, 'L', 8, 'L', 10, 'R', 6)
        main = ('A', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'C')
        self.add_inputs(main)
        self.add_inputs(moves_a)
        self.add_inputs(moves_b)
        self.add_inputs(moves_c)
        self.add_inputs('n')

        for output in self.computer.generate():
            print(chr(output), end='')
        return output


def parse(stream) -> Grid:
    return Grid(stream.readline().strip())


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        grid = parse(stream)
        grid.get_camera_view()
        result1 = grid.get_total_alignments()

    with timing("Part 2"):
        result2 = grid.run()

    return (result1, result2)
